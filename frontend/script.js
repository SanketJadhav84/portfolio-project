async function loadProjects() {

    try {

        const response = await fetch(
            "http://65.0.204.95:30050/api/messages"
        );

        const projects = await response.json();

        const container =
            document.getElementById("project-container");

        container.innerHTML = "";

        projects.forEach(project => {

            const card =
                document.createElement("div");

            card.className = "project-card";

            card.innerHTML = `
                <img src="${project.image}" alt="${project.title}">

                <div class="project-content">

                    <h3>${project.title}</h3>

                    <p>${project.description}</p>

                    <a
                        href="${project.github}"
                        target="_blank"
                        class="github-btn"
                    >
                        View Project
                    </a>

                </div>
            `;

            container.appendChild(card);

        });

    } catch(error) {
        console.log(error);
    }
}

loadProjects();

document
.getElementById("contactForm")
.addEventListener("submit", async (e) => {

    e.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        message: document.getElementById("message").value
    };

    const response = await fetch(
        "http://65.0.204.95:30050/api/messages",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(data)
        }
    );

    const result = await response.json();

    alert(result.message);

    document.getElementById("contactForm").reset();

});