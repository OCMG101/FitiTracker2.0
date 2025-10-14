document.addEventListener("DOMContentLoaded", () => {
    const formsetContainer = document.getElementById("exerciseFormset");
    const totalForms = document.getElementById("id_exercises-TOTAL_FORMS");
    const addExercisesButton = document.getElementById("addExercises");

    if (!formsetContainer || !totalForms || !addExercisesButton) {
        console.error("Missing DOM elements. Check formset and button IDs.");
        return;
    }

    // Function to build a single exercise form
    const createExerciseForm = (index) => `
        <div class="exercise-form fade-in">
            <label>Exercise Name:</label>
            <input type="text" name="exercises-${index}-exercise_name" required>

            <label>Sets:</label>
            <input type="number" name="exercises-${index}-sets" required min="1">

            <label>Reps:</label>
            <input type="number" name="exercises-${index}-reps" required min="1">

            <label>Weight (kg):</label>
            <input type="number" name="exercises-${index}-weight" required min="0">

            <button type="button" class="remove-exercise">Remove</button>
        </div>
    `;

    // Handle "Generate Forms" button click
    addExercisesButton.addEventListener("click", () => {
        const input = document.getElementById("exerciseCount");
        const count = parseInt(input.value, 10);

        if (isNaN(count) || count <= 0) {
            alert("Please enter a valid number greater than 0.");
            return;
        }

        // Clear previous forms
        formsetContainer.querySelectorAll(".exercise-form").forEach((form) => form.remove());

        // Generate new forms
        for (let i = 0; i < count; i++) {
            formsetContainer.insertAdjacentHTML("beforeend", createExerciseForm(i));
        }

        // Update Django TOTAL_FORMS
        totalForms.value = count;
    });

    // Handle removal of forms dynamically
    formsetContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-exercise")) {
            const form = e.target.closest(".exercise-form");
            if (!form) return;
            form.remove();

            // Re-index remaining forms
            const forms = formsetContainer.querySelectorAll(".exercise-form");
            forms.forEach((form, index) => {
                form.querySelectorAll("input").forEach((input) => {
                    const name = input.getAttribute("name");
                    input.setAttribute("name", name.replace(/exercises-\d+-/, `exercises-${index}-`));
                });
            });

            totalForms.value = forms.length;
        }
    });
});