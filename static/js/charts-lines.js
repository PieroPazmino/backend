/**
 * Configuración para el gráfico de líneas
 */
const lineConfig = {
  type: "line", // Tipo de gráfico: línea
  data: {
    labels: [], // Etiquetas que se llenarán con los días
    datasets: [
      {
        label: "Comentarios por día",
        backgroundColor: "#0694a2", // Color de la línea
        borderColor: "#0694a2",
        data: [], // Los datos de los comentarios por día
        fill: false, // No llenar debajo de la línea
        lineTension: 0.9, // Curvatura de la línea
      },
    ],
  },
  options: {
    responsive: true,
    legend: {
      display: false, // No mostrar leyenda
    },
    tooltips: {
      mode: "index",
      intersect: false,
    },
    hover: {
      mode: "nearest",
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: "Día", // Etiqueta para el eje X (día)
        },
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: "Número de Comentarios", // Etiqueta para el eje Y (comentarios)
        },
        beginAtZero: true, // Comenzar desde cero en el eje Y
      },
    },
  },
};

// Asignar el gráfico de líneas al contenedor
const lineCtx = document.getElementById("line");
window.myLine = new Chart(lineCtx, lineConfig);
// Función para contar los comentarios por día
countCommentsByDay = (data) => {
  // Inicializar los contadores para cada día
  const countsByDay = {}; // Objeto para almacenar el conteo de comentarios por día

  Object.values(data).forEach((record) => {
    const savedDate = record.saved; // Obtener la fecha de "saved"
    if (!savedDate) {
      return;
    }
    console.log("SAVED", savedDate.split(", ")[0]);
    // Formatear la fecha (solo tomar el día en formato dd/mm/yyyy)
    const date = new Date(savedDate.split(", ")[0]); // Usamos solo la parte de la fecha
    const formattedDate = date; // Formato 'dd/mm/yyyy'

    const dateParts = formattedDate.toLocaleString().split("/"); // Asumimos que la fecha está en "dd/mm/yyyy"

    // Comprobar si la fecha es válida
    if (dateParts.length === 3) {
      const day = dateParts[0]; // Día
      const month = dateParts[1]; // Mes
      const year = dateParts[2]; // Año

      // Crear un objeto Date con el formato "yyyy-mm-dd"
      const formattedDate = new Date(`${year}-${month}-${day}`); // Año-mes-día (yyyy-mm-dd)

      // Formatear la fecha como dd/mm/yyyy
      const formattedDateString = `${day}/${month}/${year}`;

      // Contar los comentarios por día
      if (!countsByDay[formattedDateString]) {
        countsByDay[formattedDateString] = 0;
      }
      countsByDay[formattedDateString]++;
    }
  });
  console.log("COUNTS", countsByDay);

  // Crear las etiquetas (días) y los datos (conteo de comentarios)
  const labels = Object.keys(countsByDay); // Las fechas como etiquetas
  const counts = Object.values(countsByDay); // Los conteos de comentarios por cada día

  return { labels, counts };
};

// Función para actualizar el gráfico
update = () => {
  fetch("/api/v1/landing") // Llamada a la API para obtener los datos
    .then((response) => response.json())
    .then((data) => {
      // Obtener las etiquetas (días) y los conteos de comentarios
      let { labels, counts } = countCommentsByDay(data);

      // Resetear los datos del gráfico
      window.myLine.data.labels = [];
      window.myLine.data.datasets[0].data = [];

      // Asignar los nuevos datos al gráfico
      window.myLine.data.labels = [...labels];
      window.myLine.data.datasets[0].data = [...counts];

      // Actualizar el gráfico
      window.myLine.update();
    })
    .catch((error) => console.error("Error:", error)); // Manejo de errores
};

// Llamar a la función de actualización para inicializar el gráfico
update();