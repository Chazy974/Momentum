import React, { useEffect, useState } from "react";
import { Task, fetchTasks, createTask, updateTask, deleteTask } from "../services/tasks";

function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [newDueDate, setNewDueDate] = useState("");

  useEffect(() => {
    fetchTasks()
      .then((data) => {
        const sorted = sortTasks(data);
        setTasks(sorted);
      })
      .catch(console.error);
  }, []);

  const sortTasks = (tasks: Task[]) => {
    return tasks.sort((a, b) => {
      if (a.completed !== b.completed) {
        return a.completed ? 1 : -1;
      }
      if (a.due_date && b.due_date) {
        return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
      }
      return 0;
    });
  };

  const handleAddTask = async () => {
    console.log("✅ handleAddTask déclenché");
    if (!newTask.trim()) return;

    try {
      const task = await createTask(
        newTask.trim(),
        newDescription.trim() || undefined,
        newDueDate ? new Date(newDueDate).toISOString() : undefined
      );
      const updatedTasks = sortTasks([...tasks, task]);
      setTasks(updatedTasks);
      setNewTask("");
      setNewDescription("");
      setNewDueDate("");
    } catch (err) {
      console.error("❌ Erreur dans handleAddTask :", err);
    }
  };

  const handleToggleComplete = async (task: Task) => {
    try {
      const updated = await updateTask({ ...task, completed: !task.completed });
      const updatedTasks = tasks.map(t => t.id === updated.id ? updated : t);
      setTasks(sortTasks(updatedTasks));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteTask(id);
      const updatedTasks = tasks.filter(t => t.id !== id);
      setTasks(sortTasks(updatedTasks));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Tâches</h1>
      <div className="flex flex-col gap-2 mb-4">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          className="border p-2 rounded"
          placeholder="Nouvelle tâche..."
        />
        <input
          type="text"
          value={newDescription}
          onChange={(e) => setNewDescription(e.target.value)}
          className="border p-2 rounded"
          placeholder="Description (facultative)"
        />
        <input
          type="date"
          value={newDueDate}
          onChange={(e) => setNewDueDate(e.target.value)}
          className="border p-2 rounded"
        />
        <button
          onClick={handleAddTask}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Ajouter
        </button>
      </div>
      <ul>
        {tasks.map((task) => (
          <li
            key={task.id}
            className="border-b py-2 flex justify-between items-start"
          >
            <div className="flex flex-col gap-1 w-full">
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => handleToggleComplete(task)}
                />
                <span className={task.completed ? "line-through text-gray-500" : ""}>
                  {task.title}
                </span>
              </div>
              {task.description && (
                <div className="text-sm text-gray-500 italic">{task.description}</div>
              )}
              {task.due_date && (
                <div className="text-xs text-gray-400">
                  Échéance : {new Date(task.due_date).toLocaleDateString()}
                </div>
              )}
            </div>
            <button
              onClick={() => handleDelete(task.id)}
              className="text-red-500 hover:text-red-700"
              title="Supprimer"
            >
              🗑
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Tasks;
