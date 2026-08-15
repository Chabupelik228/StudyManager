export interface StudentStatsRow {
  id: number;
  tg_id: number;
  name: string;
  total_nb: number;
  total_uv: number;
  month_nb: number;
  month_uv: number;
}

export interface StatsResponse {
  total_month_hours: number;
  total_lifetime_hours: number;
  stats: StudentStatsRow[];
}

export interface AbsenceRecord {
  date: string;
  time: string;
  name: string;
  status: number;
  reason: string;
  day_total_hours: number;
}

export interface StudentAbsencesResponse {
  absences: AbsenceRecord[];
}

export interface SubjectStatRow {
  subject: string;
  teacher: string;
  missed_month: number;
  total_month: number;
  missed_all: number;
  total_all: number;
}

export interface StudentSubjectStatsResponse {
  subjects: SubjectStatRow[];
}
