<template>
  <div>
    <Home />

    <div class="theatres-container">
      <!-- Loop through each theatre -->
      <div v-for="theatre in theatres" :key="theatre.id" class="theatre-box">
        <h2>{{ theatre.name }}</h2>
        <div class="shows-container">
          <!-- Loop through each group of three shows in the theatre.shows array -->
          <div v-for="showGroup in chunkArray(theatre.shows, 3)" :key="showGroup[0].id" class="show-row">
            <!-- Display three shows in each row -->
            <div v-for="show in showGroup" :key="show.id" class="show-item">
              <!-- Display show details -->
              <div class="show-details">
                <p><strong>Show Name:</strong> {{ show.name }}</p>
                <p><strong>Date:</strong> {{ show.date }}</p>
                <p><strong>Tags:</strong> {{ show.tags }}</p>
                <p><strong>Price:</strong> {{ show.price }}</p>
                <!-- Add more show details as needed -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Home from './Home.vue'

export default {
  name: 'UserDashboard',
  components: {
    Home
  },
  data() {
    return {
      theatres: []
    };
  },
  created() {
    this.fetchTheatres();
  },
  methods: {
    async fetchTheatres() {
      const response = await fetch(`http://127.0.0.1:5000/theatre_api`, {
        method: 'GET',
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      });

      const data = await response.json();
      if (response.ok) {
        this.theatres = data.theatres;
      } else if (response.status === 409) {
        // Handle conflict
      } else {
        this.$store.commit('setNotification', {
          variant: 'error',
          message: 'Something went wrong. Try again!!!',
        });
      }
    },
    chunkArray(arr, size) {
      // Helper method to split the array into groups of given size
      const chunkedArr = [];
      for (let i = 0; i < arr.length; i += size) {
        chunkedArr.push(arr.slice(i, i + size));
      }
      return chunkedArr;
    },
  },
};
</script>

<style>
/* Add your custom styles here */
.theatres-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.theatre-box {
  width: 100%;
  margin: 10px;
  padding: 20px;
  border: 1px solid #ccc;
  background-color: yellow;
}

.shows-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.show-row {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.show-item {
  width: calc(33.33% - 20px);
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: greenyellow;
}
</style>