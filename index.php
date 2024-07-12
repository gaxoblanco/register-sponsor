<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Company Information</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css">
    <style>
        .header-content {
            text-align: center;
            margin: 50px 0;
        }

        .header-content h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
        }

        .header-content p {
            font-size: 1.2rem;
            color: #555;
        }

        .container-flex {
            display: flex;
            width: 90%;
            margin: auto;

        }

        .container-flex input {
            margin-right: 20px;
        }

        .card-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
        }

        .card {
            width: 100%;
            max-width: 18rem;
            margin: 0.5rem;
        }

        .card img {
            max-width: 120px;
            padding: 1rem 1rem;
            margin: auto;
            display: block;
        }

        .btn {
            margin: 3px 0;
        }

        @media (min-width: 576px) {
            .card {
                flex: 0 0 calc(50% - 1rem);
            }
        }

        @media (min-width: 768px) {
            .card {
                flex: 0 0 calc(33.333% - 1rem);
            }
        }

        @media (min-width: 992px) {
            .card {
                flex: 0 0 calc(25% - 1rem);
            }
        }
    </style>
</head>

<body>
    <header class="container">
        <div class="header-content">
            <h1>Visa Sponsoring Companies in the Netherlands</h1>
            <p>Welcome to our comprehensive listing of companies in the Netherlands that sponsor visas. Here, you will find a detailed list of all companies that support visa sponsorships, along with a filter option based on the industry sector they belong to.</p>
        </div>
    </header>
    <div class="container mt-4">
        <div class="container-flex">
            <input type="text" id="search" class="form-control mb-4" placeholder="Search by industry">
            <button id="search-btn" class="btn btn-primary mb-4">Search</button>
        </div>
        <div class="card-container" id="card-container"></div>
        <nav>
            <ul class="pagination justify-content-center" id="pagination"></ul>
        </nav>
    </div>

    <?php
    // Leer el archivo JSON
    $json_data = file_get_contents('sponsors.json');
    $sponsors = json_decode($json_data, true);

    // Leer la cookie
    if (isset($_COOKIE['sponsors'])) {
        $cookie_data = json_decode($_COOKIE['sponsors'], true);
        // Actualizar el JSON original con los datos de la cookie
        foreach ($sponsors as &$sponsor) {
            foreach ($cookie_data as $cookie_sponsor) {
                if ($sponsor['id'] === $cookie_sponsor['id']) {
                    $sponsor['check'] = $cookie_sponsor['check'];
                }
            }
        }
        unset($sponsor);
    }

    // Convertir el JSON actualizado a una cadena de texto
    $json_data = json_encode($sponsors);
    ?>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const data = <?php echo $json_data; ?>;
            let filteredData = data; // Array to store filtered results
            const itemsPerPage = 10;
            let currentPage = 1;

            const setCookie = (name, value, days) => {
                const d = new Date();
                d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
                const expires = "expires=" + d.toUTCString();
                document.cookie = name + "=" + JSON.stringify(value) + ";" + expires + ";path=/";
            };

            const getCookie = (name) => {
                const value = "; " + document.cookie;
                const parts = value.split("; " + name + "=");
                if (parts.length === 2) return JSON.parse(parts.pop().split(";").shift());
                return null;
            };

            const updateCookieData = (id, checked) => {
                let cookieData = getCookie('sponsors') || [];
                const index = cookieData.findIndex(item => item.id === id);
                if (index !== -1) {
                    cookieData[index].check = checked;
                } else {
                    const sponsor = data.find(item => item.id === id);
                    if (sponsor) {
                        sponsor.check = checked;
                        cookieData.push(sponsor);
                    }
                }
                setCookie('sponsors', cookieData, 30);
            };

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
                    <figure class="text-center">
                        <img src="${item.logo_url}" class="card-img-top" alt="${item.name}">
                    </figure>
                    <div class="card-body">
                        <h5 class="card-title">${item.name}</h5>
                        <p class="card-text">${item.industry}</p>
                        <a href="${item.company_url}" class="btn btn-primary margin: 6px 0;" target="_blank">Company Info</a>
                        <a href="${item.linkedin_url}" class="btn btn-secondary" target="_blank">LinkedIn</a>
                        <button class="btn btn-${item.check ? 'success' : 'warning'} check-btn" data-id="${item.id}">
                            ${item.check ? 'Reviewed' : 'Review'}
                        </button>
                    </div>
                `;
                    container.appendChild(card);
                });

                document.querySelectorAll('.check-btn').forEach(button => {
                    button.addEventListener('click', () => {
                        const id = button.getAttribute('data-id');
                        const checked = !button.classList.contains('btn-success');
                        updateCookieData(id, checked);
                        button.classList.toggle('btn-success', checked);
                        button.classList.toggle('btn-warning', !checked);
                        button.textContent = checked ? 'Checked' : 'Check';
                    });
                });
            };

            const renderPagination = (totalItems, itemsPerPage) => {
                const totalPages = Math.ceil(totalItems / itemsPerPage);
                const pagination = document.getElementById('pagination');
                pagination.innerHTML = '';

                const createPageItem = (page) => {
                    const li = document.createElement('li');
                    li.className = 'page-item';
                    li.innerHTML = `<a class="page-link" href="#">${page}</a>`;
                    li.addEventListener('click', (e) => {
                        e.preventDefault();
                        currentPage = page;
                        renderCards(filteredData, currentPage);
                        updatePagination(totalPages);
                    });
                    return li;
                };

                if (currentPage > 1) {
                    const prevItem = createPageItem(currentPage - 1);
                    prevItem.querySelector('.page-link').innerHTML = '&laquo;';
                    pagination.appendChild(prevItem);
                }

                const startPage = Math.max(1, currentPage - 2);
                const endPage = Math.min(totalPages, currentPage + 2);

                for (let i = startPage; i <= endPage; i++) {
                    const pageItem = createPageItem(i);
                    if (i === currentPage) {
                        pageItem.classList.add('active');
                    }
                    pagination.appendChild(pageItem);
                }

                if (currentPage < totalPages) {
                    const nextItem = createPageItem(currentPage + 1);
                    nextItem.querySelector('.page-link').innerHTML = '&raquo;';
                    pagination.appendChild(nextItem);
                }
            };

            const updatePagination = (totalPages) => {
                renderPagination(filteredData.length, itemsPerPage);
            };

            const filterData = () => {
                const searchText = search.value.trim().toLowerCase();
                if (searchText === '') {
                    filteredData = data;
                } else {
                    filteredData = data.filter(item => {
                        const industryEn = item.industry_en ? item.industry_en.toLowerCase() : '';
                        return industryEn.includes(searchText);
                    });
                }
                currentPage = 1;
                renderCards(filteredData, currentPage);
                updatePagination(Math.ceil(filteredData.length / itemsPerPage));
            };

            document.getElementById('search').addEventListener('keypress', (event) => {
                if (event.key === 'Enter') {
                    filterData();
                }
            });

            document.getElementById('search-btn').addEventListener('click', () => {
                filterData();
            });


            renderCards(data, currentPage);
            renderPagination(data.length, itemsPerPage);
        });
    </script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
</body>

</html>