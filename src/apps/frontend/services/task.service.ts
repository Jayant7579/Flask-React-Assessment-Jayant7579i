import { AxiosResponse } from 'axios';

import APIService from 'frontend/services/api.service';
import { AccessToken } from 'frontend/types';

export default class TaskService extends APIService {
  getTasks = async (
    userAccessToken: AccessToken,
    page = 1,
    size = 20,
  ): Promise<AxiosResponse> =>
    this.apiClient.get(`/accounts/${userAccessToken.accountId}/tasks`, {
      headers: {
        Authorization: `Bearer ${userAccessToken.token}`,
      },
      params: {
        page,
        size,
      },
    });

  createTask = async (
    userAccessToken: AccessToken,
    title: string,
    description: string,
  ): Promise<AxiosResponse> =>
    this.apiClient.post(
      `/accounts/${userAccessToken.accountId}/tasks`,
      {
        title,
        description,
      },
      {
        headers: {
          Authorization: `Bearer ${userAccessToken.token}`,
        },
      },
    );

  updateTask = async (
    userAccessToken: AccessToken,
    taskId: string,
    title: string,
    description: string,
  ): Promise<AxiosResponse> =>
    this.apiClient.patch(
      `/accounts/${userAccessToken.accountId}/tasks/${taskId}`,
      {
        title,
        description,
      },
      {
        headers: {
          Authorization: `Bearer ${userAccessToken.token}`,
        },
      },
    );

  deleteTask = async (
    userAccessToken: AccessToken,
    taskId: string,
  ): Promise<AxiosResponse> =>
    this.apiClient.delete(
      `/accounts/${userAccessToken.accountId}/tasks/${taskId}`,
      {
        headers: {
          Authorization: `Bearer ${userAccessToken.token}`,
        },
      },
    );
}
