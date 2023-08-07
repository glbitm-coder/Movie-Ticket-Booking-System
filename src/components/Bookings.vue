<template>
    <div>
        <Home />
        <div class="bookings-container">
            <!-- Loop through bookings and generate elements for each booking -->
            <div v-for="(booking, index) in bookings" :key="index" class="booking-card">
                <!-- Display booking details here -->
                <p>Booking Serial No: {{ booking.serial_no }}</p>
                <p>Number of Tickets: {{ booking.number_of_tickets }}</p>
                <p>Total Price: {{ booking.total_price }}</p>
                <p>Show Name: {{ booking.show_name }}</p>
                <p>Theatre Name: {{ booking.theatre_name }}</p>
                <p>Date & Time: {{ booking.date_time }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import Home from './Home.vue'
import Notification from './Notification.vue'

export default {
    name: 'Bookings',
    components: {
        Home, Notification
    },
    data() {
        return {
            bookings: []
        };
    },
    created() {
    }
}
</script>

<style>
.bookings-container {
    display: flex;
    flex-wrap: wrap;
}

.booking-card {
    border: 1px solid #ccc;
    padding: 10px;
    margin: 10px;
    width: 300px;
}
</style>
