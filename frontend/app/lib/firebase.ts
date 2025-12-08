import { initializeApp, getApps, type FirebaseApp } from 'firebase/app'
import { getAuth, type Auth } from 'firebase/auth'

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDQLypmEXwXsEdnGnaZ2NDGwXr1NQgi3rY",
  authDomain: "nerdie-85d0a.firebaseapp.com",
  projectId: "nerdie-85d0a",
  storageBucket: "nerdie-85d0a.firebasestorage.app",
  messagingSenderId: "626685033991",
  appId: "1:626685033991:web:1c1f36e0e0a0b0fa1c1f36"
}

// Initialize Firebase
let app: FirebaseApp
let auth: Auth

if (!getApps().length) {
  app = initializeApp(firebaseConfig)
} else {
  app = getApps()[0]
}

auth = getAuth(app)

export { app, auth }
