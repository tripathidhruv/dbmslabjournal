-- ============================================================
-- DBMS Lab Journal — COMPLETE FIX SCRIPT
-- Run this ENTIRE script in Supabase SQL Editor
-- This replaces everything — safe to run multiple times
-- ============================================================


-- ============================================================
-- STEP 1: CONFIRM ALL EXISTING UNCONFIRMED USERS
-- (Fixes "please confirm email" on existing accounts)
-- ============================================================
UPDATE auth.users
SET email_confirmed_at = COALESCE(email_confirmed_at, now()),
    updated_at = now()
WHERE email_confirmed_at IS NULL;


-- ============================================================
-- STEP 2: DROP ALL OLD POLICIES (clean slate)
-- ============================================================
DROP POLICY IF EXISTS "Users can view own profile" ON profiles;
DROP POLICY IF EXISTS "Staff can view all profiles" ON profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
DROP POLICY IF EXISTS "Students can view own submissions" ON practical_submissions;
DROP POLICY IF EXISTS "Staff can view all submissions" ON practical_submissions;
DROP POLICY IF EXISTS "Students can insert own submissions" ON practical_submissions;
DROP POLICY IF EXISTS "Students can update own submissions" ON practical_submissions;
DROP POLICY IF EXISTS "Students can update own pending submissions" ON practical_submissions;
DROP POLICY IF EXISTS "Staff can update any submission" ON practical_submissions;


-- ============================================================
-- STEP 3: SECURITY DEFINER HELPER FUNCTION
-- Breaks infinite recursion: calling is_staff() from within
-- a profiles policy won't re-trigger the same policy.
-- ============================================================
CREATE OR REPLACE FUNCTION public.is_staff()
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
STABLE
SET search_path = public
AS $$
  SELECT EXISTS (
    SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'staff'
  );
$$;


-- ============================================================
-- STEP 4: RECREATE PROFILES TABLE (if not exists) + RLS
-- ============================================================
CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT NOT NULL DEFAULT 'User',
  role TEXT NOT NULL DEFAULT 'student' CHECK (role IN ('student', 'staff')),
  roll_number TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Simple, non-recursive policies
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Staff can view all profiles"
  ON profiles FOR SELECT USING (public.is_staff());

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Staff can update any profile"
  ON profiles FOR UPDATE USING (public.is_staff());


-- ============================================================
-- STEP 5: PRACTICAL SUBMISSIONS TABLE + RLS
-- ============================================================
CREATE TABLE IF NOT EXISTS practical_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  practical_number INT NOT NULL CHECK (practical_number BETWEEN 1 AND 14),
  code_file_url TEXT,
  screenshot_url TEXT,
  submitted_at TIMESTAMPTZ DEFAULT now(),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  staff_remarks TEXT,
  reviewed_by UUID REFERENCES profiles(id),
  reviewed_at TIMESTAMPTZ,
  UNIQUE(student_id, practical_number)
);

ALTER TABLE practical_submissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Students can view own submissions"
  ON practical_submissions FOR SELECT USING (auth.uid() = student_id);

CREATE POLICY "Staff can view all submissions"
  ON practical_submissions FOR SELECT USING (public.is_staff());

CREATE POLICY "Students can insert own submissions"
  ON practical_submissions FOR INSERT WITH CHECK (auth.uid() = student_id);

CREATE POLICY "Students can update own submissions"
  ON practical_submissions FOR UPDATE USING (auth.uid() = student_id);

CREATE POLICY "Staff can update any submission"
  ON practical_submissions FOR UPDATE USING (public.is_staff());


-- ============================================================
-- STEP 6: AUTO-CREATE PROFILE ON SIGNUP (trigger)
-- ============================================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, role, roll_number)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)),
    COALESCE(NEW.raw_user_meta_data->>'role', 'student'),
    NULLIF(NEW.raw_user_meta_data->>'roll_number', '')
  )
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();


-- ============================================================
-- STEP 7: CREATE/UPDATE STAFF ACCOUNT
-- ============================================================
DO $$
DECLARE
  staff_uid UUID;
BEGIN
  -- Check if staff user already exists
  SELECT id INTO staff_uid FROM auth.users WHERE email = 'admin@dbmslab.edu';

  IF staff_uid IS NULL THEN
    -- Create fresh staff account, pre-confirmed
    INSERT INTO auth.users (
      instance_id, id, aud, role, email,
      encrypted_password, email_confirmed_at,
      raw_app_meta_data, raw_user_meta_data,
      created_at, updated_at,
      confirmation_token, email_change,
      email_change_token_new, recovery_token
    ) VALUES (
      '00000000-0000-0000-0000-000000000000',
      gen_random_uuid(), 'authenticated', 'authenticated',
      'admin@dbmslab.edu',
      crypt('Admin@123', gen_salt('bf')),
      now(),
      '{"provider":"email","providers":["email"]}',
      '{"full_name":"Lab Administrator","role":"staff"}',
      now(), now(), '', '', '', ''
    ) RETURNING id INTO staff_uid;

    RAISE NOTICE 'Staff user created with id: %', staff_uid;
  ELSE
    RAISE NOTICE 'Staff user already exists with id: %', staff_uid;
  END IF;

  -- Upsert staff profile
  INSERT INTO profiles (id, full_name, role, roll_number)
  VALUES (staff_uid, 'Lab Administrator', 'staff', NULL)
  ON CONFLICT (id) DO UPDATE
    SET role = 'staff', full_name = 'Lab Administrator', roll_number = NULL;

  RAISE NOTICE 'Staff profile set. Login: admin@dbmslab.edu / Admin@123';
END $$;


-- ============================================================
-- STEP 8: ALSO CREATE PROFILES FOR EXISTING AUTH USERS
-- who signed up but whose profile wasn't created (e.g. if
-- the trigger wasn't installed yet when they signed up)
-- ============================================================
INSERT INTO profiles (id, full_name, role)
SELECT
  u.id,
  COALESCE(u.raw_user_meta_data->>'full_name', split_part(u.email, '@', 1)),
  COALESCE(u.raw_user_meta_data->>'role', 'student')
FROM auth.users u
WHERE NOT EXISTS (SELECT 1 FROM profiles p WHERE p.id = u.id)
ON CONFLICT (id) DO NOTHING;


-- ============================================================
-- STEP 9: STORAGE BUCKET
-- ============================================================
INSERT INTO storage.buckets (id, name, public)
VALUES ('practical-uploads', 'practical-uploads', false)
ON CONFLICT (id) DO UPDATE SET public = false;

-- Drop old storage policies
DROP POLICY IF EXISTS "Students upload own files" ON storage.objects;
DROP POLICY IF EXISTS "Users read own files" ON storage.objects;
DROP POLICY IF EXISTS "Staff read all files" ON storage.objects;
DROP POLICY IF EXISTS "Students update own files" ON storage.objects;
DROP POLICY IF EXISTS "Students delete own files" ON storage.objects;

-- Allow all authenticated users to upload to their own folder
CREATE POLICY "Students upload own files"
  ON storage.objects FOR INSERT TO authenticated
  WITH CHECK (
    bucket_id = 'practical-uploads'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Users read own files"
  ON storage.objects FOR SELECT TO authenticated
  USING (
    bucket_id = 'practical-uploads'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Staff read all files"
  ON storage.objects FOR SELECT TO authenticated
  USING (
    bucket_id = 'practical-uploads'
    AND public.is_staff()
  );

CREATE POLICY "Students update own files"
  ON storage.objects FOR UPDATE TO authenticated
  USING (
    bucket_id = 'practical-uploads'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Students delete own files"
  ON storage.objects FOR DELETE TO authenticated
  USING (
    bucket_id = 'practical-uploads'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );


-- ============================================================
-- VERIFY: Check what was created
-- ============================================================
SELECT 'auth.users' as tbl, count(*) FROM auth.users
UNION ALL
SELECT 'profiles', count(*) FROM profiles
UNION ALL
SELECT 'practical_submissions', count(*) FROM practical_submissions;
