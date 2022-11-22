// Imports
const axios = require('axios')

// API key
const API_KEY = '<YOUR_API_KEY>' // Get your API key here: https://app.fliki.ai/account/api

// API URL
const API_URL = 'https://api.fliki.ai/v1'

// Language list
async function languageList() {
  try {
    const { data } = await axios({
      method: 'get',
      url: `${API_URL}/languages`,
      headers: {
        Authentication: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    })

    return data ? data.data : null
  } catch (error) {
    console.log(error)
  }

  return null
}

// Dialect list
async function dialectList() {
  try {
    const { data } = await axios({
      method: 'get',
      url: `${API_URL}/dialects`,
      headers: {
        Authentication: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    })

    return data ? data.data : null
  } catch (error) {
    console.log(error)
  }

  return null
}

// Voice list
async function voiceList({ languageId, dialectId }) {
  try {
    const { data } = await axios({
      method: 'post',
      url: `${API_URL}/voices`,
      headers: {
        Authentication: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      data: {
        languageId,
        dialectId,
      },
    })

    return data ? data.data : null
  } catch (error) {
    console.log(error)
  }

  return null
}

// Generate audio
async function generateAudio({ content, voiceId, voiceStyleId = null }) {
  try {
    const { data } = await axios({
      method: 'post',
      url: `${API_URL}/generate/audio`,
      headers: {
        Authentication: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      data: {
        content,
        voiceId,
        voiceStyleId,
      },
    })

    return data ? data.data : null
  } catch (error) {
    console.log(error)
  }

  return null
}

// Usage
async function usage() {
  try {
    const { data } = await axios({
      method: 'get',
      url: `${API_URL}/usage`,
      headers: {
        Authentication: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    })

    return data ? data.data : null
  } catch (error) {
    console.log(error)
  }

  return null
}

;(async () => {
  // Get languages
  if (true) {
    const languages = await languageList()
    console.log('languages', languages)
  }

  // Get dialects
  if (false) {
    const dialects = await dialectList()
    console.log('dialects', dialects)
  }

  // Get voices
  if (false) {
    const voices = await voiceList({
      languageId: '61b8b2f54268666c126babc9', // English
      dialectId: '61b8b31c4268666c126bace7', // United States
    })
    console.log('voices', voices)
  }

  // Generate audio
  if (false) {
    const audio = await generateAudio({
      content: 'Hello, thank you for giving Fliki API a try!',
      voiceId: '61b8b45a4268666c126bb32b', // English, United States, Sara
    })

    console.log('audio', audio)
  }

  // Get usage
  if (false) {
    const data = await usage()

    console.log('data', data)
  }
})()
