<template>
  <div class="events-container">
    <h3>Derniers événements réseau</h3>
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
.events-container {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 800px;
  margin-top: 20px;
}

h3 {
  text-align: center;
  margin-bottom: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}

li:last-child {
  border-bottom: none;
}
</style>
