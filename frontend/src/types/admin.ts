export interface AdminUser {
  id: number;
  name: string;
  is_online: boolean;
  last_seen: number;
}

export interface AdminUsersResponse {
  admins: AdminUser[];
}

export interface ActionLogItem {
  id: number;
  admin_name: string;
  action_type: string;
  details: string;
  created_at: number;
}

export interface AdminLogsResponse {
  logs: ActionLogItem[];
  filter_users: string[];
  filter_actions: string[];
}
