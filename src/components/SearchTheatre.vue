<template>
    <div>
      <Home />
  
      <div class="search-container">
        <h1>Search Theatre</h1>
        <div class="search-input">
          <label for="location">Location:</label>
          <input type="text" id="location" v-model="searchLocation" />
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="searchName" />
          <b-btn variant="primary" @click="searchTheatres">Search</b-btn>
        </div>
        <!-- ... Existing search box and search button code ... -->
  
        <div class="theatres-container">
    <template v-for="rowTheatres in chunkArray(theatres, 3)">
      <div class="theatre-row">
        <div v-for="(theatre, index) in rowTheatres" :key="index" class="theatre-item">
          <img class="show-image" :src="getImageUrl(theatre.image)" />
          <h2> {{theatre.name}}</h2>
          <p>Location : {{ theatre.place }}</p>
          <p>Capacity : {{ theatre.capacity }}</p>
        </div>
      </div>
    </template>
  </div>
      </div>
    </div>
  </template>
  
  <script>
  import Home from './Home.vue'
  
  export default {
    name: 'SearchTheatre',
    components: {
      Home
    },
    data() {
      return {
        theatres: [],
        searchLocation: "",
        searchName: ""
      };
    },
    methods: {
      // ... Existing search methods ...
      chunkArray(arr, size) {
        // Helper method to split the array into groups of given size
        const chunkedArr = [];
        for (let i = 0; i < arr.length; i += size) {
          chunkedArr.push(arr.slice(i, i + size));
        }
        return chunkedArr;
      },
      getImageUrl(imagePath) {
            return require(`../assets/images/${imagePath}`)
        },
      async searchTheatres() {
        const user_id = parseInt(localStorage.getItem('userId')); 
        const response = await fetch(`http://127.0.0.1:5000/search/user/${user_id}/theatres?input_name=${this.searchName}&input_location=${this.searchLocation}`, {
        method: "GET",
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          "Content-Type": "application/json"
        }
      }).then(async result => {
        const data = await result.json();
        if (result.ok) {
          this.theatres = data.theatres;
        }
        else {
          this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
        }
      })
      }
    }
  };
  </script>
  
  <style scoped>
  /* ... Existing styles ... */
  
  .theatre-row {
    width: 100%;
    display: flex;
    margin-bottom: 20px;
  }
  
  .theatre-item {
    width: calc(33.33% - 10px);
    padding: 10px;
    border: 1px solid #ccc;
    background-color: greenyellow;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* Add the margin property to create space between theatres */
    margin-right: 10px;
  }
  .search-container {
    padding: 20px;
  }
  
  .search-input {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .theatres-container {
    display: flex;
    flex-wrap: wrap;
  }
  .show-image{
    width: 420px;
    height: 220px;
  }

  /* Add more custom styles as needed */
  </style>