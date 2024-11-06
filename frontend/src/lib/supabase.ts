import { createClient } from '@supabase/supabase-js';
import type { Database } from './database.types';

const publicSupabaseUrl = 'https://rdwmjwfivqjkbsipxlih.supabase.co';
const publicAnonKey =
	'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJkd21qd2ZpdnFqa2JzaXB4bGloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA5MDU3NTgsImV4cCI6MjA0NjQ4MTc1OH0.mdOp2-DXwBA1hc54_ne-IzrG_qdnuqtYw6j9M4B5JkU';

export const supabase = createClient<Database>(publicSupabaseUrl, publicAnonKey);
