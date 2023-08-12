<template>
    <div>
        <Home/>
        <div class="summary-container">
            <h1>Select Theatre</h1>
            <div class="search-input">
                <b-dropdown id="theatre-dropdown" :text="current_theatre ? current_theatre.name : 'Select Theatre'" variant="outline-success">
                    <b-dropdown-item v-for="theatre in theatres" :key="theatre.id" :value="theatre.name" @click="selectTheatre(theatre)">
                        {{ theatre.name }}
                    </b-dropdown-item>
                </b-dropdown>
            </div>
            <br/>
            <br/>
            <div v-if="showImages" class="summary-images">
                <div class="image-container">
                    <img src="../assets/summary/theatre_tickets_sold.png" class="image" />
                </div>
                <div class="image-container">
                    <img src="../assets/summary/theatre_average_ratings.png" class="image" />
                </div>
                <div class="image-container">
                    <img src="../assets/summary/theatre_total_prices.png" class="image" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Home from './Home.vue'
import Notification from './Notification.vue'
import { BDropdown, BDropdownItem } from 'bootstrap-vue';

export default {
    name: 'Summary',
    components: {
        Home, Notification, BDropdown, BDropdownItem
    },
    data() {
        return {
            theatres: [],
            current_theatre: null,
            ticketsSoldImage: '',
            averageRatingsImage: '',
            totalPricesImage: '',
            showImages: false,
            averageRatingsImageName: ''
        };
    },
    mounted(){ 
        this.fetchTheatres(); 
    },
    methods: {
        async fetchTheatres() {
            const user_id = parseInt(localStorage.getItem('userId'));
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre_api`, {
                method: "GET",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                }
            }).then(async result => {
                const data = await result.json();
                if (result.ok) {
                    this.theatres = data.theatres;
                }
                else if (result.status === 409) {

                }
                else {
                    this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                }
            })
        },
        async selectTheatre(theatre) {
            this.showImages=false;
            this.current_theatre = theatre;
            const user_id = parseInt(localStorage.getItem('userId'));
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre/${this.current_theatre.id}/summary_api`, {
                method: "GET",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                }
            });
            if (response.ok) {
                this.showImages = true;
            }
            else if (result.status === 409) {

            }
            else {
                this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
            }
        },
    }
}


</script>

<style >

.summary-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    height: 100vh;
    padding-top: 20px;
}

.search-input {
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 20px;
}

.summary-images {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

.image-container {
    margin: 10px;
    border: 1px solid #ccc; /* Add border to the image container */
}

.image {
    max-width: 100%;
    height: auto;
    border: 5px solid #dd1313; /* Add border to the image */
}


</style>