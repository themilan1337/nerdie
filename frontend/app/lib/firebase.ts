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

console.log('🔥 [FIREBASE] Initializing Firebase...')
console.log('🔥 [FIREBASE] Config:', {
  apiKey: firebaseConfig.apiKey.substring(0, 20) + '...',
  authDomain: firebaseConfig.authDomain,
  projectId: firebaseConfig.projectId
})

// Initialize Firebase
let app: FirebaseApp
let auth: Auth

if (!getApps().length) {
  console.log('🔥 [FIREBASE] No existing app, creating new Firebase app...')
  app = initializeApp(firebaseConfig)
  console.log('✅ [FIREBASE] Firebase app created')
} else {
  console.log('🔥 [FIREBASE] Using existing Firebase app')
  app = getApps()[0]
}

auth = getAuth(app)
console.log('✅ [FIREBASE] Auth instance created')
console.log('🔥 [FIREBASE] Auth config:', auth.config)
console.log('🔥 [FIREBASE] Auth name:', auth.name)

export { app, auth }
