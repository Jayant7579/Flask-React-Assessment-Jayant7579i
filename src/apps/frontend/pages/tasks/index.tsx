import React, { useCallback, useEffect, useMemo, useState } from 'react';
import toast from 'react-hot-toast';

import Button from 'frontend/components/button';
import FormControl from 'frontend/components/form-control';
import Input from 'frontend/components/input';
import VerticalStackLayout from 'frontend/components/layouts/vertical-stack-layout';
import TaskService from 'frontend/services/task.service';
import { Task } from 'frontend/types';
import { ButtonKind, ButtonType } from 'frontend/types/button';
import { JsonObject } from 'frontend/types/common-types';
import { getAccessTokenFromStorage } from 'frontend/utils/storage-util';

type TaskFormState = {
  title: string;
  description: string;
};

const defaultFormState: TaskFormState = {
  title: '',
  description: '',
};

const taskService = new TaskService();

const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [deletingTaskId, setDeletingTaskId] = useState<string | null>(null);
  const [createForm, setCreateForm] = useState<TaskFormState>(defaultFormState);
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState<TaskFormState>(defaultFormState);

  const taskCountLabel = useMemo(
    () => `${tasks.length} task${tasks.length === 1 ? '' : 's'}`,
    [tasks.length],
  );

  const fetchTasks = useCallback(async () => {
    const accessToken = getAccessTokenFromStorage();
    if (!accessToken) {
      toast.error('You need to log in again to view tasks.');
      return;
    }

    setIsLoading(true);
    try {
      const response = await taskService.getTasks(accessToken);
      const items = (response.data?.items || []) as JsonObject[];
      const mappedTasks = items.map((item) => new Task(item));
      setTasks(mappedTasks);
    } catch (error) {
      toast.error('Failed to load tasks. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreate = async () => {
    const title = createForm.title.trim();
    const description = createForm.description.trim();

    if (!title) {
      toast.error('Title is required.');
      return;
    }

    if (!description) {
      toast.error('Description is required.');
      return;
    }

    const accessToken = getAccessTokenFromStorage();
    if (!accessToken) {
      toast.error('You need to log in again to create tasks.');
      return;
    }

    setIsCreating(true);
    try {
      const response = await taskService.createTask(
        accessToken,
        title,
        description,
      );
      const createdTask = new Task(response.data as JsonObject);
      setTasks((prev) => [createdTask, ...prev]);
      setCreateForm(defaultFormState);
      toast.success('Task created.');
    } catch (error) {
      toast.error('Failed to create task. Please try again.');
    } finally {
      setIsCreating(false);
    }
  };

  const handleStartEdit = (task: Task) => {
    setEditingTaskId(task.id);
    setEditForm({ title: task.title, description: task.description });
  };

  const handleCancelEdit = () => {
    setEditingTaskId(null);
    setEditForm(defaultFormState);
  };

  const handleUpdate = async () => {
    const title = editForm.title.trim();
    const description = editForm.description.trim();

    if (!editingTaskId) {
      return;
    }

    if (!title) {
      toast.error('Title is required.');
      return;
    }

    if (!description) {
      toast.error('Description is required.');
      return;
    }

    const accessToken = getAccessTokenFromStorage();
    if (!accessToken) {
      toast.error('You need to log in again to update tasks.');
      return;
    }

    setIsUpdating(true);
    try {
      const response = await taskService.updateTask(
        accessToken,
        editingTaskId,
        title,
        description,
      );
      const updatedTask = new Task(response.data as JsonObject);
      setTasks((prev) =>
        prev.map((task) => (task.id === updatedTask.id ? updatedTask : task)),
      );
      setEditingTaskId(null);
      setEditForm(defaultFormState);
      toast.success('Task updated.');
    } catch (error) {
      toast.error('Failed to update task. Please try again.');
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async (taskId: string) => {
    const accessToken = getAccessTokenFromStorage();
    if (!accessToken) {
      toast.error('You need to log in again to delete tasks.');
      return;
    }

    setDeletingTaskId(taskId);
    try {
      await taskService.deleteTask(accessToken, taskId);
      setTasks((prev) => prev.filter((task) => task.id !== taskId));
      toast.success('Task deleted.');
    } catch (error) {
      toast.error('Failed to delete task. Please try again.');
    } finally {
      setDeletingTaskId(null);
    }
  };

  return (
    <div className="min-h-screen bg-whiten px-4 py-6">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-6">
        <div className="rounded-lg border border-stroke bg-white p-6 shadow-card">
          <div className="mb-6">
            <h1 className="text-title-md2 font-semibold text-black">Tasks</h1>
            <p className="text-sm text-body">
              Create and manage your tasks with quick edits.
            </p>
          </div>

          <VerticalStackLayout gap={4}>
            <FormControl label="Title">
              <Input
                placeholder="Write a short task title"
                value={createForm.title}
                onChange={(event) =>
                  setCreateForm((prev) => ({
                    ...prev,
                    title: event.target.value,
                  }))
                }
              />
            </FormControl>

            <FormControl label="Description">
              <div className="w-full rounded-lg border border-stroke bg-white p-4 outline-none focus-within:border-primary">
                <textarea
                  className="min-h-[120px] w-full resize-none outline-none"
                  placeholder="Add a helpful description"
                  value={createForm.description}
                  onChange={(event) =>
                    setCreateForm((prev) => ({
                      ...prev,
                      description: event.target.value,
                    }))
                  }
                />
              </div>
            </FormControl>

            <div className="flex justify-end">
              <div className="w-40">
                <Button
                  type={ButtonType.BUTTON}
                  kind={ButtonKind.PRIMARY}
                  isLoading={isCreating}
                  onClick={handleCreate}
                >
                  Add Task
                </Button>
              </div>
            </div>
          </VerticalStackLayout>
        </div>

        <div className="rounded-lg border border-stroke bg-white p-6 shadow-card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-black">Your Tasks</h2>
            <span className="text-sm text-body">{taskCountLabel}</span>
          </div>

          {isLoading ? (
            <div className="py-10 text-center text-body">Loading tasks...</div>
          ) : tasks.length === 0 ? (
            <div className="rounded-md border border-dashed border-stroke p-8 text-center text-body">
              No tasks yet. Add your first task above.
            </div>
          ) : (
            <div className="flex flex-col gap-4">
              {tasks.map((task) => {
                const isEditing = editingTaskId === task.id;
                return (
                  <div
                    key={task.id}
                    className="rounded-lg border border-stroke bg-gray-3 p-4"
                  >
                    {isEditing ? (
                      <VerticalStackLayout gap={4}>
                        <FormControl label="Title">
                          <Input
                            value={editForm.title}
                            onChange={(event) =>
                              setEditForm((prev) => ({
                                ...prev,
                                title: event.target.value,
                              }))
                            }
                          />
                        </FormControl>
                        <FormControl label="Description">
                          <div className="w-full rounded-lg border border-stroke bg-white p-4 outline-none focus-within:border-primary">
                            <textarea
                              className="min-h-[100px] w-full resize-none outline-none"
                              value={editForm.description}
                              onChange={(event) =>
                                setEditForm((prev) => ({
                                  ...prev,
                                  description: event.target.value,
                                }))
                              }
                            />
                          </div>
                        </FormControl>
                        <div className="flex items-center justify-end gap-3">
                          <button
                            className="text-sm font-medium text-body"
                            onClick={handleCancelEdit}
                            type="button"
                          >
                            Cancel
                          </button>
                          <div className="w-32">
                            <Button
                              type={ButtonType.BUTTON}
                              kind={ButtonKind.PRIMARY}
                              isLoading={isUpdating}
                              onClick={handleUpdate}
                            >
                              Save
                            </Button>
                          </div>
                        </div>
                      </VerticalStackLayout>
                    ) : (
                      <div className="flex flex-col gap-3">
                        <div>
                          <h3 className="text-base font-semibold text-black">
                            {task.title}
                          </h3>
                          <p className="text-sm text-body">
                            {task.description}
                          </p>
                        </div>
                        <div className="flex flex-wrap items-center gap-4">
                          <button
                            className="text-sm font-medium text-primary disabled:cursor-not-allowed disabled:opacity-60"
                            onClick={() => handleStartEdit(task)}
                            type="button"
                            disabled={isUpdating}
                          >
                            Edit
                          </button>
                          <button
                            className="text-sm font-medium text-danger disabled:cursor-not-allowed disabled:opacity-60"
                            onClick={() => handleDelete(task.id)}
                            type="button"
                            disabled={deletingTaskId === task.id}
                          >
                            {deletingTaskId === task.id
                              ? 'Deleting...'
                              : 'Delete'}
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Tasks;
