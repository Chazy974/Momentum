import { useEffect, useState } from "react";
import { Task, fetchTasks, createTask } from "../services/tasks";

function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState("");

  useEffect(() => {
    fetchTasks().then(setTasks).catch(console.error);
  }, []);

  const handleAddTask = async () => {
    if (!newTask.trim()) return;
    try {
      const task = await createTask(newTask.trim());
      setTasks([...tasks, task]);
      setNewTask("");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Tâches</h1>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          className="border p-2 flex-1 rounded"
          placeholder="Nouvelle tâche..."
        />
        <button
          onClick={handleAddTask}
          className="bg-blue-500 text-white px-4 rounded"
        >
          Ajouter
        </button>
      </div>
      <ul>
        {tasks.map((task) => (
          <li
            key={task.id}
            className="border-b py-2 flex justify-between items-center"
          >
            <span>{task.title}</span>
            {task.completed && <span className="text-green-500">✓</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Tasks;