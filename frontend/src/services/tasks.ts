export interface Task {
  id: number;
  title: string;
  description?: string;
  due_date?: string;
  completed: boolean;
}

export async function fetchTasks(): Promise<Task[]> {
  const res = await fetch("http://localhost:8000/tasks/");
  if (!res.ok) throw new Error("Erreur lors du chargement des tâches");
  return res.json();
}

export async function createTask(title: string): Promise<Task> {
  const res = await fetch("http://localhost:8000/tasks/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, completed: false }),
  });
  if (!res.ok) throw new Error("Erreur lors de la création");
  return res.json();
}

export async function updateTask(task: Task): Promise<Task> {
  const res = await fetch(`http://localhost:8000/tasks/${task.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task),
  });
  if (!res.ok) throw new Error("Erreur lors de la mise à jour");
  return res.json();
}

export async function deleteTask(id: number): Promise<void> {
  const res = await fetch(`http://localhost:8000/tasks/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Erreur lors de la suppression");
}