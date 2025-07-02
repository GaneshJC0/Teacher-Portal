// Dashboard page functionality
document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const addStudentBtn = document.getElementById('addStudentBtn');
    const studentModal = document.getElementById('studentModal');
    const deleteModal = document.getElementById('deleteModal');
    const studentForm = document.getElementById('studentForm');
    const studentsTableBody = document.getElementById('studentsTableBody');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const noStudentsMessage = document.getElementById('noStudentsMessage');
    const modalTitle = document.getElementById('modalTitle');
    const saveBtn = document.getElementById('saveBtn');
    const saveSpinner = document.getElementById('saveSpinner');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const deleteSpinner = document.getElementById('deleteSpinner');

    // State
    let currentStudentId = null;
    let isEditMode = false;
    let students = [];

    // Initialize dashboard
    init();

    async function init() {
        await loadStudents();
        setupEventListeners();
    }

    // Setup event listeners
    function setupEventListeners() {
        // Add student button
        addStudentBtn.addEventListener('click', () => {
            openStudentModal();
        });

        // Modal close buttons
        document.getElementById('closeModalBtn').addEventListener('click', closeStudentModal);
        document.getElementById('cancelBtn').addEventListener('click', closeStudentModal);
        document.getElementById('closeDeleteModalBtn').addEventListener('click', closeDeleteModal);
        document.getElementById('cancelDeleteBtn').addEventListener('click', closeDeleteModal);

        // Form submission
        studentForm.addEventListener('submit', handleStudentFormSubmit);

        // Delete confirmation
        confirmDeleteBtn.addEventListener('click', handleDeleteStudent);

        // Close modals when clicking outside
        studentModal.addEventListener('click', (e) => {
            if (e.target === studentModal) {
                closeStudentModal();
            }
        });

        deleteModal.addEventListener('click', (e) => {
            if (e.target === deleteModal) {
                closeDeleteModal();
            }
        });

        // Form field validation
        ['studentName', 'subjectName', 'marks'].forEach(fieldId => {
            document.getElementById(fieldId).addEventListener('input', () => {
                Utils.clearError(fieldId.replace('student', '').replace('subject', 'subject').toLowerCase() + 'Error');
                Utils.clearError('formError');
            });
        });
    }

    // Load students from API
    async function loadStudents() {
        try {
            showLoadingOverlay(true);
            const response = await API.get('/api/students');
            
            if (response.success) {
                students = response.students || [];
                renderStudentsTable();
            } else {
                Toast.error(response.message || 'Failed to load students');
            }
        } catch (error) {
            console.error('Error loading students:', error);
            Toast.error('Failed to load students');
        } finally {
            showLoadingOverlay(false);
        }
    }

    // Render students table
    function renderStudentsTable() {
        if (students.length === 0) {
            studentsTableBody.innerHTML = '';
            noStudentsMessage.style.display = 'block';
            return;
        }

        noStudentsMessage.style.display = 'none';
        
        studentsTableBody.innerHTML = students.map(student => `
            <tr data-student-id="${student.id}">
                <td class="student-name">${escapeHtml(student.name)}</td>
                <td class="student-subject">${escapeHtml(student.subject_name)}</td>
                <td class="student-marks">${student.marks}</td>
                <td class="student-actions">
                    <button class="edit-btn" onclick="editStudent(${student.id})" title="Edit Student">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="m18.5 2.5 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                    </button>
                    <button class="delete-btn" onclick="deleteStudent(${student.id})" title="Delete Student">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3,6 5,6 21,6"></polyline>
                            <path d="m19,6 v14 a2,2 0 0,1 -2,2 H7 a2,2 0 0,1 -2,-2 V6 m3,0 V4 a2,2 0 0,1 2,-2 h4 a2,2 0 0,1 2,2 v2"></path>
                            <line x1="10" y1="11" x2="10" y2="17"></line>
                            <line x1="14" y1="11" x2="14" y2="17"></line>
                        </svg>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    // Open student modal for adding/editing
    function openStudentModal(student = null) {
        isEditMode = !!student;
        currentStudentId = student ? student.id : null;
        
        modalTitle.textContent = isEditMode ? 'Edit Student' : 'Add Student';
        
        // Reset form
        studentForm.reset();
        Utils.clearFormErrors('studentForm');
        
        if (isEditMode && student) {
            document.getElementById('studentId').value = student.id;
            document.getElementById('studentName').value = student.name;
            document.getElementById('subjectName').value = student.subject_name;
            document.getElementById('marks').value = student.marks;
        }
        
        studentModal.style.display = 'flex';
        document.getElementById('studentName').focus();
    }

    // Close student modal
    function closeStudentModal() {
        studentModal.style.display = 'none';
        currentStudentId = null;
        isEditMode = false;
    }

    // Handle student form submission
    async function handleStudentFormSubmit(e) {
        e.preventDefault();
        
        // Clear previous errors
        Utils.clearFormErrors('studentForm');
        
        // Get form data
        const formData = new FormData(studentForm);
        const studentData = {
            name: formData.get('name').trim(),
            subject_name: formData.get('subject_name').trim(),
            marks: parseInt(formData.get('marks'))
        };
        
        // Validate fields
        let isValid = true;
        
        if (!Utils.validateField('studentName', 'nameError', 'required')) {
            isValid = false;
        }
        
        if (!Utils.validateField('subjectName', 'subjectError', 'required')) {
            isValid = false;
        }
        
        if (!Utils.validateField('marks', 'marksError', 'marks')) {
            isValid = false;
        }
        
        if (!isValid) {
            return;
        }
        
        // Show loading state
        Utils.showButtonLoading(saveBtn, saveSpinner);
        
        try {
            let response;
            
            if (isEditMode && currentStudentId) {
                response = await API.put(`/api/students/${currentStudentId}`, studentData);
            } else {
                response = await API.post('/api/students', studentData);
            }
            
            if (response.success) {
                Toast.success(isEditMode ? 'Student updated successfully!' : 'Student added successfully!');
                closeStudentModal();
                await loadStudents(); // Reload the table
            } else {
                Utils.showError('formError', response.message || 'Failed to save student');
            }
        } catch (error) {
            console.error('Error saving student:', error);
            Utils.showError('formError', error.message || 'An error occurred while saving');
        } finally {
            Utils.hideButtonLoading(saveBtn, saveSpinner);
        }
    }

    // Edit student
    window.editStudent = function(studentId) {
        const student = students.find(s => s.id === studentId);
        if (student) {
            openStudentModal(student);
        }
    };

    // Delete student
    window.deleteStudent = function(studentId) {
        const student = students.find(s => s.id === studentId);
        if (student) {
            currentStudentId = studentId;
            document.getElementById('deleteStudentInfo').innerHTML = 
                `<strong>${escapeHtml(student.name)}</strong> - ${escapeHtml(student.subject_name)} (${student.marks} marks)`;
            deleteModal.style.display = 'flex';
        }
    };

    // Handle delete student
    async function handleDeleteStudent() {
        if (!currentStudentId) return;
        
        Utils.showButtonLoading(confirmDeleteBtn, deleteSpinner);
        
        try {
            const response = await API.delete(`/api/students/${currentStudentId}`);
            
            if (response.success) {
                Toast.success('Student deleted successfully!');
                closeDeleteModal();
                await loadStudents(); // Reload the table
            } else {
                Toast.error(response.message || 'Failed to delete student');
            }
        } catch (error) {
            console.error('Error deleting student:', error);
            Toast.error(error.message || 'An error occurred while deleting');
        } finally {
            Utils.hideButtonLoading(confirmDeleteBtn, deleteSpinner);
        }
    }

    // Close delete modal
    function closeDeleteModal() {
        deleteModal.style.display = 'none';
        currentStudentId = null;
    }

    // Show/hide loading overlay
    function showLoadingOverlay(show) {
        loadingOverlay.style.display = show ? 'flex' : 'none';
    }

    // Utility function to escape HTML
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }
});