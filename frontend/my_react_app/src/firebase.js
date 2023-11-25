// firebase.js
import { initializeApp } from 'firebase/app';
import { getAuth} from 'firebase/auth';

const firebaseConfig = {
    apiKey: "AIzaSyD-1tNwD_9STQNAlM7jEvl4QTd1ZZoEyvw",
    authDomain: "fyp-ulugbek.firebaseapp.com",
    projectId: "fyp-ulugbek",
    storageBucket: "fyp-ulugbek.appspot.com",
    messagingSenderId: "95545326321",
    appId: "1:95545326321:web:da0f15f381652795f80750",
    measurementId: "G-CME6NTE191"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth};
