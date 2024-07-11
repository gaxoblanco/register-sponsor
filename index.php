<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Company Information</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css">
    <style>
        .card-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
        }
        .card {
            width: 18rem;
        }
    </style>
</head>
<body>

<div class="container mt-4">
    <div class="card-container" id="card-container"></div>
    <nav>
        <ul class="pagination justify-content-center" id="pagination"></ul>
    </nav>
</div>

<?php
// Leer el archivo JSON
$json_data = file_get_contents('sponsors.json');
?>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        const data = <?php echo $json_data; ?>;
        const itemsPerPage = 10;
        let currentPage = 1;

        const renderCards = (data, page = 1) => {
            const container = document.getElementById('card-container');
            container.innerHTML = '';

            const start = (page - 1) * itemsPerPage;
            const end = page * itemsPerPage;
            const items = data.slice(start, end);

            items.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <img src="${item.logo_url}" class="card-img-top" alt="${item.name}">
                    <div class="card-body">
                        <h5 class="card-title">${item.name}</h5>
                        <p class="card-text">${item.industry}</p>
                        <a href="${item.company_url}" class="btn btn-primary" target="_blank">Company Info</a>
                        <a href="${item.linkedin_url}" class="btn btn-secondary" target="_blank">LinkedIn</a>
                    </div>
                `;
                container.appendChild(card);
            });
        };

        const renderPagination = (totalItems, itemsPerPage) => {
            const totalPages = Math.ceil(totalItems / itemsPerPage);
            const pagination = document.getElementById('pagination');
            pagination.innerHTML = '';

            for (let i = 1; i <= totalPages; i++) {
                const li = document.createElement('li');
                li.className = 'page-item';
                li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
                li.addEventListener('click', () => {
                    currentPage = i;
                    renderCards(data, currentPage);
                    updatePagination();
                });
                pagination.appendChild(li);
            }
        };

        const updatePagination = () => {
            const paginationItems = document.querySelectorAll('.page-item');
            paginationItems.forEach((item, index) => {
                item.classList.toggle('active', index === currentPage - 1);
            });
        };

        renderCards(data, currentPage);
        renderPagination(data.length, itemsPerPage);
        updatePagination();
    });
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
</body>
</html>
