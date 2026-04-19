/* ── Data ───────────────────────────────────────── */
let editIndex = null;

let students = [
    { first: 'Amara', last: 'Osei', age: 16, cls: '10-A', email: 'amara@school.edu', gpa: 3.8, status: 'Active' },
    { first: 'Lucas', last: 'Ferreira', age: 15, cls: '10-B', email: 'lucas@school.edu', gpa: 3.2, status: 'Active' },
    { first: 'Mei', last: 'Zhang', age: 17, cls: '9-C', email: 'mei@school.edu', gpa: 3.9, status: 'Active' },
    { first: 'Daniel', last: 'Moreau', age: 16, cls: '11-D', email: 'dan@school.edu', gpa: 2.8, status: 'Inactive' },
    { first: 'Priya', last: 'Nair', age: 15, cls: '10-A', email: 'priya@school.edu', gpa: 3.5, status: 'Active' },
    { first: 'Carlos', last: 'Vega', age: 17, cls: '9-C', email: 'carlos@school.edu', gpa: 3.1, status: 'Active' },
    { first: 'Sofia', last: 'Andersen', age: 16, cls: '10-B', email: 'sofia@school.edu', gpa: 3.7, status: 'Active' },
    { first: 'Tariq', last: 'Hassan', age: 18, cls: '11-D', email: 'tariq@school.edu', gpa: 2.5, status: 'Inactive' },
];

const gradesData = [
    { name: 'Amara Osei', cls: '10-A', math: 92, sci: 88, eng: 95, hist: 85 },
    { name: 'Lucas Ferreira', cls: '10-B', math: 74, sci: 81, eng: 70, hist: 78 },
    { name: 'Mei Zhang', cls: '9-C', math: 97, sci: 94, eng: 89, hist: 91 },
    { name: 'Daniel Moreau', cls: '11-D', math: 65, sci: 70, eng: 72, hist: 68 },
    { name: 'Priya Nair', cls: '10-A', math: 85, sci: 88, eng: 91, hist: 82 },
    { name: 'Carlos Vega', cls: '9-C', math: 78, sci: 82, eng: 76, hist: 80 },
    { name: 'Sofia Andersen', cls: '10-B', math: 88, sci: 85, eng: 90, hist: 87 },
    { name: 'Tariq Hassan', cls: '11-D', math: 60, sci: 65, eng: 68, hist: 62 },
];

const classesData = [
    { name: 'Mathematics 10-A', teacher: 'Mr. Ahmed', students: 22, avg: 87, color: 'green' },
    { name: 'Science 10-B', teacher: 'Ms. Laurent', students: 20, avg: 81, color: 'amber' },
    { name: 'English 9-C', teacher: 'Mr. Okafor', students: 25, avg: 83, color: 'coral' },
    { name: 'History 11-D', teacher: 'Ms. Park', students: 18, avg: 75, color: 'blue' },
    { name: 'Physics 10-A', teacher: 'Dr. Patel', students: 22, avg: 79, color: 'green' },
    { name: 'Biology 9-C', teacher: 'Ms. Russo', students: 25, avg: 84, color: 'amber' },
];

/* ── Helpers ────────────────────────────────────── */
const colors = ['#2D6A4F', '#D4A017', '#C26B4B', '#3B63C7', '#52B788', '#885B3A'];
const classPill = c => { const m = { '10-A': 'a', '10-B': 'b', '9-C': 'c', '11-D': 'd' }; return m[c] || 'a'; };

function initial(s) { return (s.first[0] || '') + (s.last[0] || ''); }

function gradeLetterClass(v) {
    if (v >= 90) return 'a'; if (v >= 80) return 'b'; if (v >= 70) return 'c'; if (v >= 60) return 'd'; return 'f';
}
function gradeLetter(v) {
    if (v >= 90) return 'A'; if (v >= 80) return 'B'; if (v >= 70) return 'C'; if (v >= 60) return 'D'; return 'F';
}

/* ── Render Students ────────────────────────────── */
function renderStudents() {
    const body = document.getElementById('studentsBody');
    body.innerHTML = students.map((s, i) => `
    <tr>
      <td>
        <div class="avatar-name">
          <div class="name-badge" style="background:${colors[i % colors.length]}">${initial(s)}</div>
          ${s.first} ${s.last}
        </div>
      </td>
      <td>${s.age}</td>
      <td><span class="class-pill ${classPill(s.cls)}">${s.cls}</span></td>
      <td>${s.gpa.toFixed(1)}</td>
      <td>
        <span class="class-pill ${s.status === 'Active' ? 'a' : 'c'}">${s.status}</span>
      </td>
      <td>
        <div class="actions">
          <button class="btn-icon edit" onclick="openModal(${i})" title="Edit">
            <svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          </button>
          <button class="btn-icon danger" onclick="deleteStudent(${i})" title="Delete">
            <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

/* ── Render Classes ─────────────────────────────── */
function renderClasses() {
    document.getElementById('classesGrid').innerHTML = classesData.map(c => `
    <div class="class-card">
      <div class="class-card-header">
        <div class="class-letter ${c.color}">${c.name.charAt(0)}</div>
        <span class="class-pill ${c.color === 'green' ? 'a' : c.color === 'amber' ? 'b' : c.color === 'coral' ? 'c' : 'd'}">${c.students} students</span>
      </div>
      <div class="class-card-name">${c.name}</div>
      <div class="class-card-teacher">${c.teacher}</div>
      <div class="class-meta">
        <div class="class-meta-item">
          <span class="class-meta-val">${c.students}</span>
          <span class="class-meta-lbl">Students</span>
        </div>
        <div class="class-meta-item">
          <span class="class-meta-val">${c.avg}%</span>
          <span class="class-meta-lbl">Avg Grade</span>
        </div>
      </div>
    </div>
  `).join('');
}

/* ── Render Grades ──────────────────────────────── */
function filterGrades() {
    const filter = document.getElementById('gradeFilter').value;
    const data = filter === 'all' ? gradesData : gradesData.filter(g => g.cls === filter);
    document.getElementById('gradesBody').innerHTML = data.map((g, i) => {
        const avg = Math.round((g.math + g.sci + g.eng + g.hist) / 4);
        return `<tr>
      <td><div class="avatar-name">
        <div class="name-badge" style="background:${colors[i % colors.length]}">${g.name.split(' ').map(w => w[0]).join('')}</div>
        ${g.name}</div></td>
      <td><span class="class-pill ${classPill(g.cls)}">${g.cls}</span></td>
      <td><span class="grade-badge ${gradeLetterClass(g.math)}">${g.math}</span></td>
      <td><span class="grade-badge ${gradeLetterClass(g.sci)}">${g.sci}</span></td>
      <td><span class="grade-badge ${gradeLetterClass(g.eng)}">${g.eng}</span></td>
      <td><span class="grade-badge ${gradeLetterClass(g.hist)}">${g.hist}</span></td>
      <td><span class="grade-badge ${gradeLetterClass(avg)}">${gradeLetter(avg)}</span></td>
    </tr>`;
    }).join('');
}

/* ── Chart ──────────────────────────────────────── */
function renderChart() {
    const ctx = document.getElementById('perfChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
            datasets: [{
                label: 'Class Average',
                data: [74, 78, 76, 82, 80, 84],
                backgroundColor: '#EBF5EF',
                borderColor: '#2D6A4F',
                borderWidth: 2,
                borderRadius: 6,
            }, {
                label: 'Top Performers',
                data: [88, 91, 90, 95, 94, 97],
                backgroundColor: '#FBF4E0',
                borderColor: '#D4A017',
                borderWidth: 2,
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top', labels: { font: { family: 'DM Sans', size: 12 }, boxWidth: 10 } },
                tooltip: { bodyFont: { family: 'DM Sans' }, titleFont: { family: 'DM Sans' } }
            },
            scales: {
                y: {
                    beginAtZero: false, min: 60, max: 100, grid: { color: '#E5E3DC' },
                    ticks: { font: { family: 'DM Sans', size: 11 } }
                },
                x: { grid: { display: false }, ticks: { font: { family: 'DM Sans', size: 11 } } }
            }
        }
    });
}

/* ── Navigation ─────────────────────────────────── */
function navigate(e, id) {
    e.preventDefault();
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.getElementById('page-' + id).classList.add('active');
    e.currentTarget.classList.add('active');
    if (window.innerWidth <= 768) document.body.classList.remove('sidebar-open');
}

/* ── Sidebar ────────────────────────────────────── */
function toggleSidebar() {
    if (window.innerWidth <= 768) {
        document.body.classList.toggle('sidebar-open');
    } else {
        document.body.classList.toggle('sidebar-collapsed');
    }
}


/* ── Modal ──────────────────────────────────────── */

let currentEditId = null;  // To store the ID of the student we want to edit

function openModal(studentId) {
    if (studentId !== undefined && studentId !== null) {
        // Edit mode - we need to fetch student data from the server
        currentEditId = studentId;
        document.getElementById('modalTitle').textContent = 'Edit Student';

        // Send a request to fetch this specific student's data
        fetch(`/get_student/${studentId}`)
            .then(response => response.json())
            .then(student => {
                document.getElementById('fName').value = student.first_name;
                document.getElementById('lName').value = student.last_name;
                document.getElementById('sAge').value = student.age;
                document.getElementById('sClass').value = student.class;
                document.getElementById('sEmail').value = student.email;
                document.getElementById('sGpa').value = student.phone;  // phone
                document.getElementById('sStatus').value = student.status;
            })
            .catch(error => console.error('Error:', error));
    } else {
        // Add mode
        currentEditId = null;
        document.getElementById('modalTitle').textContent = 'Add Student';
        // Clear the fields
        document.getElementById('fName').value = '';
        document.getElementById('lName').value = '';
        document.getElementById('sAge').value = '';
        document.getElementById('sClass').value = '10-A';
        document.getElementById('sEmail').value = '';
        document.getElementById('sGpa').value = '';
        document.getElementById('sStatus').value = 'Active';
    }

    document.getElementById('modal').classList.add('open');
}

function closeModal() {
    document.getElementById('modal').classList.remove('open');
    currentEditId = null;
}

function saveStudent(event) {
    // Prevent the default form submission
    event.preventDefault();

    const formData = {
        first_name: document.getElementById('fName').value,
        last_name: document.getElementById('lName').value,
        age: document.getElementById('sAge').value,
        class: document.getElementById('sClass').value,
        email: document.getElementById('sEmail').value,
        number_phone: document.getElementById('sGpa').value,
        status: document.getElementById('sStatus').value
    };

    let url = '/add_student';
    let method = 'POST';

    if (currentEditId !== null) {
        // Editing
        url = `/edit_student/${currentEditId}`;
        method = 'POST';
    }

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
        .then(response => {
            if (response.ok) {
                closeModal();
                window.location.reload();  // Reload the page to display updated data
            }
        })
        .catch(error => console.error('Error:', error));
}

// function openModal(idx) {
//     editIndex = (idx !== undefined) ? idx : null;
//     document.getElementById('modalTitle').textContent = editIndex !== null ? 'Edit Student' : 'Add Student';
//     if (editIndex !== null) {
//         const s = students[editIndex];
//         document.getElementById('fName').value = s.first;
//         document.getElementById('lName').value = s.last;
//         document.getElementById('sAge').value = s.age;
//         document.getElementById('sClass').value = s.cls;
//         document.getElementById('sEmail').value = s.email;
//         document.getElementById('sGpa').value = s.gpa;
//         document.getElementById('sStatus').value = s.status;
//     } else {
//         ['fName', 'lName', 'sAge', 'sEmail', 'sGpa'].forEach(id => document.getElementById(id).value = '');
//         document.getElementById('sStatus').value = 'Active';
//     }
//     document.getElementById('modal').classList.add('open');
// }

function closeModal() {
    document.getElementById('modal').classList.remove('open');
    editIndex = null;
}

document.getElementById('modal').addEventListener('click', e => {
    if (e.target === e.currentTarget) closeModal();
});

function saveStudent() {
    const first = document.getElementById('fName').value.trim();
    const last = document.getElementById('lName').value.trim();
    const age = parseInt(document.getElementById('sAge').value);
    if (!first || !last || !age) { showToast('Please fill required fields.'); return; }
    const s = {
        first, last, age,
        cls: document.getElementById('sClass').value,
        email: document.getElementById('sEmail').value,
        gpa: parseFloat(document.getElementById('sGpa').value) || 0,
        status: document.getElementById('sStatus').value,
    };
    if (editIndex !== null) { students[editIndex] = s; showToast('Student updated!'); }
    else { students.push(s); showToast('Student added!'); }
    renderStudents();
    closeModal();
}

function deleteStudent(i) {
    students.splice(i, 1);
    renderStudents();
    showToast('Student removed.');
}

/* ── Toast ──────────────────────────────────────── */
function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2800);
}

/* ── Init ───────────────────────────────────────── */
renderStudents();
renderClasses();
filterGrades();
renderChart();