/**
 * Supabase database types — matches the schema in supabase/migrations/001_initial_schema.sql.
 *
 * In production you'd auto-generate this with `supabase gen types typescript`.
 * For now this hand-written version keeps us moving.
 */

import type { MathAnalysis } from '../context/AppContext';

export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          display_name: string | null;
          grade_level: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id: string;
          display_name?: string | null;
          grade_level?: string | null;
        };
        Update: {
          display_name?: string | null;
          grade_level?: string | null;
        };
        Relationships: [];
      };
      tutoring_sessions: {
        Row: {
          id: string;
          user_id: string;
          title: string;
          preview: string | null;
          subject: string | null;
          mode: string | null;
          photo_url: string | null;
          analysis: MathAnalysis | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          title: string;
          preview?: string | null;
          subject?: string | null;
          mode?: string | null;
          photo_url?: string | null;
          analysis?: MathAnalysis | null;
        };
        Update: {
          title?: string;
          preview?: string | null;
          subject?: string | null;
          mode?: string | null;
          photo_url?: string | null;
          analysis?: MathAnalysis | null;
        };
        Relationships: [];
      };
      session_messages: {
        Row: {
          id: string;
          session_id: string;
          role: 'user' | 'assistant';
          content: string;
          image_url: string | null;
          sort_order: number;
          created_at: string;
        };
        Insert: {
          id?: string;
          session_id: string;
          role: 'user' | 'assistant';
          content: string;
          image_url?: string | null;
          sort_order: number;
        };
        Update: {
          content?: string;
          image_url?: string | null;
          sort_order?: number;
        };
        Relationships: [];
      };
      saved_items: {
        Row: {
          id: string;
          user_id: string;
          image_url: string;
          analysis: MathAnalysis;
          created_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          image_url: string;
          analysis: MathAnalysis;
        };
        Update: {
          image_url?: string;
          analysis?: MathAnalysis;
        };
        Relationships: [];
      };
    };
    Views: {};
    Functions: {};
    Enums: {};
    CompositeTypes: {};
  };
}
