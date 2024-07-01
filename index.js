const puppeteer = require("puppeteer");
const fs = require("fs");

const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(
  "525047294790-ehi410okqs7ll9njldt115iiucpit8au.apps.googleusercontent.com"
);

// Función para buscar en Google y obtener los resultados usando SerpApi
const searchGoogle = async (query) => {
  return new Promise((resolve, reject) => {
    search.json(
      {
        q: query,
        location: "Austin, TX",
      },
      (data) => {
        if (data) {
          resolve(data);
        } else {
          reject("No data received");
        }
      }
    );
  });
};

// Duck scraper
const searchDuck = async (query) => {
  // navegamos a https://duckduckgo.com/?t=h_&q=Flynth+Audit+B.V.+linkein&ia=web
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  //convierto los spaces en +
  query = query.replace(" ", "+");
  await page.goto(`https://duckduckgo.com/?t=h_&q=${query}+linkein&ia=web`);
  //imprimo por consola toda la pagina
  // console.log(await page.content());

  // busco el article con id r1-0
  const result = await page.evaluate(() => {
    return document.querySelector("article#r1-0");
  });
  // si lo encuentro busco el href de la etiqueta a dentro del article
  if (result) {
    const link = await page.evaluate(() => {
      return document.querySelector("article#r1-0 a").href;
    });
    console.log(`Encontrado en DuckDuckGo: ${link}`);
    // impirmimos un hola mundo
  } else {
    console.log(`No encontrado en DuckDuckGo`);
  }
};

// Función para buscar patrocinadores en una página y luego buscar en Google
const searchSponsors = async (url, text) => {
  console.log(`Buscando patrocinadores en: ${url}`);
  try {
    // Lanzamos un navegador con Puppeteer
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Navegamos a la URL proporcionada
    await page.goto(url);

    // Esperamos a que el selector de la tabla esté presente en la página
    await page.waitForSelector("tbody");

    // Evaluamos el contenido de la página para extraer los nombres de los patrocinadores
    const sponsors = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll("tbody tr"));
      return rows.map((row) => {
        const th = row.querySelector("th");
        return th ? th.innerText : "";
      });
    });

    // Filtramos los patrocinadores que contienen el texto buscado, ignorando mayúsculas y minúsculas
    const filteredSponsors = sponsors.filter((sponsor) =>
      sponsor.toLowerCase().includes(text.toLowerCase())
    );

    // Transformamos el array en un objeto con claves como los nombres y valores como texto vacío
    const sponsorsObject = {};
    filteredSponsors.forEach((sponsor) => {
      sponsorsObject[sponsor] = "";
    });

    // Creamos un archivo .json con el nombre del texto buscado y cargamos los patrocinadores filtrados
    if (filteredSponsors.length > 0) {
      const fileName = `${text}.json`;
      const data = JSON.stringify(sponsorsObject, null, 2); // Convertimos el objeto a JSON con formato

      // Escribimos el archivo JSON
      fs.writeFileSync(fileName, data, "utf8");
      console.log(`Archivo ${fileName} creado con éxito.`);
    } else {
      console.log(
        `No se encontraron patrocinadores que contengan el texto: ${text}`
      );
    }

    // Itero por el json para buscar en searchDuck
    for (const key in filteredSponsors) {
      //console.log(`${key}: ${sponsorsObject[key]}`);
      await searchDuck(key);
    }
    // Cerramos el navegador
    await browser.close();
  } catch (error) {
    console.log(`Error: ${error}`);
  }
};

// Llamar a la función de búsqueda de patrocinadores
searchSponsors(
  "https://ind.nl/en/public-register-recognised-sponsors/public-register-regular-labour-and-highly-skilled-migrants",
  "technologies"
);
