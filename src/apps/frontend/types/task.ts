import { JsonObject } from 'frontend/types/common-types';

export class Task {
  id: string;
  accountId: string;
  title: string;
  description: string;

  constructor(json: JsonObject) {
    this.id = json.id as string;
    this.accountId = json.account_id as string;
    this.title = json.title as string;
    this.description = json.description as string;
  }
}

export type PaginationParams = {
  page: number;
  size: number;
};

export type PaginatedTaskResponse = {
  items: Task[];
  pagination_params: PaginationParams;
  total_count: number;
  total_pages: number;
};
