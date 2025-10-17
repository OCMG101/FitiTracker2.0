document.addEventListener("DOMContentLoaded", () => {
  const addExercisesBtn = document.getElementById("addExercises");
  const formsetContainer = document.getElementById("exerciseFormset");
  const loadTemplateBtn = document.getElementById("loadTemplateBtn");
  const workoutNameInput = document.getElementById("id_name");

  function createExerciseForm(index) {
    const div = document.createElement("div");
    div.classList.add("exercise-form");

    div.innerHTML = `
      <label>Muscle Group:</label>
      <select class="muscle-group">
        <option value="">Select group</option>
        ${window.exerciseCategories
          .map(cat => `<option value="${cat}">${cat}</option>`)
          .join("")}
      </select>

      <label>Exercise:</label>
      <select name="form-${index}-exercise_name" class="exercise-dropdown">
        <option value="">Select exercise</option>
      </select>

      <input type="number" name="form-${index}-sets" placeholder="Sets" required>
      <input type="number" name="form-${index}-reps" placeholder="Reps" required>
      <input type="number" name="form-${index}-weight" placeholder="Weight (kg)" required>
    `;

    div.querySelector(".muscle-group").addEventListener("change", (e) => {
      const category = e.target.value;
      fetch(`/get_exercises_by_category/?category=${category}`)
        .then(res => res.json())
        .then(data => {
          const exerciseDropdown = div.querySelector(".exercise-dropdown");
          exerciseDropdown.innerHTML = `<option value="">Select exercise</option>`;
          data.forEach(name => {
            const opt = document.createElement("option");
            opt.value = name;
            opt.textContent = name;
            exerciseDropdown.appendChild(opt);
          });
        });
    });

    formsetContainer.appendChild(div);
  }

  addExercisesBtn.addEventListener("click", () => {
    const count = parseInt(document.getElementById("exerciseCount").value);
    formsetContainer.innerHTML = "";
    for (let i = 0; i < count; i++) createExerciseForm(i);
  });

  loadTemplateBtn.addEventListener("click", () => {
    const workoutName = workoutNameInput.value.trim();
    if (!workoutName) return alert("Enter a workout name first!");

    fetch(`/get_workout_template/?name=${workoutName}`)
      .then(res => res.json())
      .then(exercises => {
        if (!exercises.length) return alert("No saved template found.");

        formsetContainer.innerHTML = "";
        exercises.forEach((ex, i) => {
          createExerciseForm(i);
          const form = formsetContainer.lastElementChild;
          form.querySelector(".exercise-dropdown").innerHTML =
            `<option selected value="${ex.exercise_name}">${ex.exercise_name}</option>`;
          form.querySelector(`input[name="form-${i}-sets"]`).value = ex.sets;
          form.querySelector(`input[name="form-${i}-reps"]`).value = ex.reps;
          form.querySelector(`input[name="form-${i}-weight"]`).value = ex.weight;
        });
      });
  });

  // preload categories from backend-rendered list
  window.exerciseCategories = JSON.parse('{{ categories|safe|escapejs }}');
});
