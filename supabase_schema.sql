-- CloudCull AI - Supabase Schema
-- Run this in your Supabase SQL Editor (SQL Editor -> New Query -> Paste -> Run)

-- Handle RLS for users
-- Ensure 'apps' table exists with appropriate columns

CREATE TABLE IF NOT EXISTS public.apps (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
    tool_name text NOT NULL,
    department text,
    monthly_cost numeric DEFAULT 0,
    total_seats integer DEFAULT 0,
    active_users integer DEFAULT 0,
    status text DEFAULT 'Active',
    last_used date DEFAULT CURRENT_DATE,
    renewal_date date DEFAULT (CURRENT_DATE + interval '30 days'),
    created_at timestamp with time zone DEFAULT now()
);

-- Enable RLS (Row Level Security)
ALTER TABLE public.apps ENABLE ROW LEVEL SECURITY;

-- Create policy for users to see only their own data
CREATE POLICY "Users can only see their own apps" 
ON public.apps 
FOR ALL 
USING (auth.uid() = user_id);

-- Create a policy for users to insert their own data
CREATE POLICY "Users can only insert their own apps" 
ON public.apps 
FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- Create a policy for users to update their own data
CREATE POLICY "Users can only update their own apps" 
ON public.apps 
FOR UPDATE 
USING (auth.uid() = user_id);

-- Provide a quick summary query to check if it's working
-- SELECT COUNT(*) FROM public.apps;
