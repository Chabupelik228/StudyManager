export interface DutyStudent {
  id: number;
  name: string;
  tg_id: number;
  date: string | null;
  is_absent_now: boolean;
}

export interface DutiesResponse {
  duties: DutyStudent[];
}

export interface DutyAssignRequest {
  date: string;
  student_ids: number[];
}
