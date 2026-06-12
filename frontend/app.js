const taskForm = document.getElementById('taskForm');
const tasksDiv = document.getElementById('tasks');
const planPre = document.getElementById('plan');
const statusDiv = document.getElementById('status');
const clearBtn = document.getElementById('clearBtn');
const generateBtn = document.getElementById('generateBtn');

function escapeHtml(str) {
  return String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '<')
    .replaceAll('>', '>')
    .replaceAll('"', '"')
    .replaceAll("'", '&#039;');
}

async function fetchTasks() {
  tasksDiv.textContent = 'Loading...';
  const res = await fetch('/api/tasks');
  const data = await res.json();

  const tasks = data.tasks || [];
  if (!tasks.length) {
    tasksDiv.innerHTML = '<div class="muted">No tasks found. Add one above.</div>';
    return;
  }

  tasksDiv.innerHTML = '';
  tasks.forEach((t) => {
    const el = document.createElement('div');
    el.className = 'task-item';
    el.innerHTML = `
      <div><b>${escapeHtml(t.subject || '')}</b></div>
      <div class="muted">Deadline: ${escapeHtml(t.deadline || '')} | Priority: ${escapeHtml(t.priority || '')} | Est: ${escapeHtml(t.estimated_hours ?? '')} hrs</div>
      <div>${escapeHtml(t.description || '')}</div>
    `;
    tasksDiv.appendChild(el);
  });
}

async function addTask(e) {
  e.preventDefault();

  const formData = new FormData(taskForm);
  const payload = {
    subject: formData.get('subject'),
    description: formData.get('description'),
    deadline: formData.get('deadline'),
    priority: formData.get('priority'),
    estimated_hours: Number(formData.get('estimated_hours')),
  };

  statusDiv.textContent = 'Adding task...';
  const res = await fetch('/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) {
    statusDiv.textContent = data.error || 'Failed to add task.';
    return;
  }

  statusDiv.textContent = 'Task added.';
  taskForm.reset();
  await fetchTasks();
}

async function clearTasks() {
  const ok = confirm('Type OK to clear all tasks.');
  if (!ok) return;

  statusDiv.textContent = 'Clearing tasks...';
  const res = await fetch('/api/tasks', { method: 'DELETE' });
  const data = await res.json();

  if (!res.ok) {
    statusDiv.textContent = data.error || 'Failed to clear tasks.';
    return;
  }

  statusDiv.textContent = 'All tasks cleared.';
  planPre.textContent = ' ';
  await fetchTasks();
}

async function generatePlan() {
  statusDiv.textContent = 'Generating plan...';
  planPre.textContent = ' ';

  const res = await fetch('/api/plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ max_hours_per_day: 4.0 }),
  });

  const data = await res.json();
  if (!res.ok) {
    statusDiv.textContent = data.error || 'Failed to generate plan.';
    planPre.textContent = ' ';
    return;
  }

  statusDiv.textContent = data.used_llm ? 'AI plan generated.' : 'Heuristic plan generated (LLM not used).';
  planPre.textContent = data.plan || '';
}

taskForm.addEventListener('submit', addTask);
clearBtn.addEventListener('click', clearTasks);
generateBtn.addEventListener('click', generatePlan);

fetchTasks();

