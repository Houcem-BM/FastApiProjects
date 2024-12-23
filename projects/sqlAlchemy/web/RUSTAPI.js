const apiUrl = "http://localhost:8000/students/";


function reloadFunc(){
  location.reload(); 
  document.getElementById("log_out").style.display ="none";
}

document.querySelector("#checkUser").addEventListener("submit",async (e)=>{
    e.preventDefault();
    const userName = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${apiUrl}${userName}`,{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ userName, password }),
        });
    const data = await response.json();
    if (data.message == "welcome") {
        alert("welcome");
        document.getElementById("checkUser").style.display = "none"; 
        document.querySelector("#content").style.display ="block";
        document.getElementById("log_out").style.display ="block";
        fetchStudents();
        } else {
        alert("access denied");
        }

    })



    
// Fetch and display students
async function fetchStudents() {
	
    const response = await fetch(apiUrl);
    const students = await response.json();

    const tbody = document.querySelector("#studentTable tbody");

    tbody.innerHTML ="";

    students.forEach(student => {
        tbody.innerHTML += `<tr>
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.grade}</td>
                <td>  <button onclick = deleteStudent("${student.id}") >Delete </button>   
                      <!-- <button  onclick = "updateStudent(${student.id},'${student.name}',${student.grade}, this)" >Update </button>  </td>-->
                      <button  id="update-${student.id}"  onclick = "updateStudent(${student.id},'${student.name}',${student.grade})" >Update </button>     </td>
        
            </tr>`
    });
}
fetchStudents();


// Add a new student
document.getElementById("addStudentForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("studentName").value;
    const grade = document.getElementById("studentGrade").value;

    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, grade: parseInt(grade) }),
    });

    if (response.ok) {
      alert(response.message);
      document.getElementById("studentName").value = "";
      document.getElementById("studentGrade").value = "";
      console.log("added successfully");
      fetchStudents();
    } else {
      alert("Failed to add student.");
    }
  });

// Update student

async function updateStudent(student_id, student_name, student_grade/*, button*/) {
    //button.style.display = 'none';
    document.getElementById(`update-${student_id}`).style.display = "none";
    document.querySelector(".updateStudentForm").style.display = "block";
  
    document.getElementById("updateId").value = student_id;
    document.getElementById("updateName").value = student_name;
    document.getElementById("updateGrade").value = student_grade;

    document.getElementById("updateStudentForm").addEventListener("submit", async (e) => {
        e.preventDefault();
  
        const id = document.getElementById("updateId").value;
        const name = document.getElementById("updateName").value;
        const grade = document.getElementById("updateGrade").value;
  
        const response = await fetch(`${apiUrl}${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: parseInt(id), name, grade: parseInt(grade) }),
        });
  
        if (response.ok) {
          alert("Student updated successfully!");
          fetchStudents();
          document.querySelector(".updateStudentForm").style.display = "none";
        } else {
          alert("Failed to update student. Student not found.");
        }
      });  
}


// Delete a student

async function deleteStudent(id) {

    const response = await fetch(`${apiUrl}${id}`,{
        method : "DELETE",
    });
    if (response.ok) {
        alert("Student deleted successfully!");
        fetchStudents();
      } else {
        alert("Failed to delete student. Student not found.");
      }
    
}
