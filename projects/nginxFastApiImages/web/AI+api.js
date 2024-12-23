const form = document.getElementById("predictionForm");
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const formData = new FormData(form);
            console.log(formData)
            const queryParams = new URLSearchParams(formData).toString();
            console.log(queryParams)
            const apiUrl = `http://127.0.0.0:8000/predict?${queryParams}`;
            
            try {
                const response = await fetch(apiUrl);
                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById("result").innerText = `Predicted Grade: ${result["الدرجة المتوقعة"]}`;
                } else {
                    document.getElementById("result").innerText = `Error: ${result.error}`;
                }
            } catch (error) {
                document.getElementById("result").innerText = "An error occurred while fetching the prediction.";
            }
        });
