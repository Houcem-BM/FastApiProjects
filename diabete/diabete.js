const form = document.getElementById("predictForm");
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const formData = new FormData(form);
            const queryParams = new URLSearchParams(formData).toString();
            const apiUrl = `http://127.0.0.1:8000/predict?${queryParams}`;
            
            try {
                const response = await fetch(apiUrl);
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById("result").innerText = `احتمال الاصابة بداء السكري: ${data["result"]}`;
                } else {
                    document.getElementById("result").innerText = `Error: ${data.error}`;
                }
            } catch (error) {
                document.getElementById("result").innerText = "An error occurred while fetching the prediction.";
            }
        });