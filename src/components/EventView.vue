<template>
  <div class="events-container">
    <h3>📡 Derniers événements réseau</h3>
    <ul>
      <li v-for="event in events" :key="event.id">
        <strong>{{ event.type }}</strong> - {{ event.timestamp }}
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  name: "NetworkEvents",
  setup() {
    const events = ref([]);

    const fetchEvents = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/events");
        events.value = response.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des événements :", error);
      }
    };

    onMounted(fetchEvents);

    return { events };
  },
};
</script>

<style scoped>
/* Conteneur principal */
.events-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: white;
  width: 100%;
  max-width: 60vw; /* Limite la largeur max */
  height: auto;
  padding: 3vh;
  border-radius: 1vh;
  overflow: auto;
  max-height: 100%;
}

/* Titre */
h3 {
  text-align: center;
  font-size: calc(1.2rem + 0.5vw); /* Ajuste la taille dynamiquement */
  margin-bottom: 2vh;
}

/* Liste des événements */
ul {
  list-style-type: none;
  padding: 0;
  width: 100%;
}

/* Élément de la liste */
li {
  padding: 1.5vh;
  font-size: calc(0.8rem + 0.3vw); /* Taille dynamique */
  border-bottom: 0.3vh solid #ddd;
  display: flex;
  justify-content: space-between;
  width: 100%;
}

/* Supprimer la bordure du dernier élément */
li:last-child {
  border-bottom: none;
}
</style>
