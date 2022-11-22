<?php

require 'util.php';

// API key
define('API_KEY', '<YOUR_API_KEY>'); // Get your API key here: https://app.fliki.ai/account/api

// API endpoint
define('API_URL', 'https://api.fliki.ai/v1');

// Language list
function languageList() {
  try {
    $endpoint = 'languages';

    $response = curl($endpoint, 'get');

    if($response) {
      $languages = json_decode($response);

      return $languages->data;
    }
  } catch (Exception $error) {
    echo $error;
  }

  return null;
}

// Dialect list
function dialectList() {
  try {
    $endpoint = 'dialects';

    $response = curl($endpoint, 'get');

    if($response) {
      $dialects = json_decode($response);

      return $dialects->data;
    }
  } catch (Exception $error) {
    echo $error;
  }

  return null;
}

// Voice list
function voiceList($languageId, $dialectId) {
  try {
    $endpoint = 'voices';

    $data = array(
      'languageId' => $languageId,
      'dialectId' => $dialectId,
    );

    $response = curl($endpoint, 'post', $data);

    if($response) {
      $voices = json_decode($response);

      return $voices->data;
    }
  } catch (Exception $error) {
    echo $error;
  }

  return null;
}

// Generate audio
function generateAudio($content, $voiceId, $voiceStyleId = null) {
  try {
    $endpoint = 'generate/audio';

    $data = array(
      'content' => $content,
      'voiceId' => $voiceId,
    );

    if($voiceStyleId) {
      $data['voiceStyleId'] = $voiceStyleId;
    }

    $response = curl($endpoint, 'post', $data);

    if($response) {
      $result = json_decode($response);

      return $result->data;
    }
  } catch (Exception $error) {
    echo $error;
  }

  return null;
}

(function() {
  // Get languages
  if(true) {
    $languages = languageList();
    print_r($languages);
  }

  // Get dialects
  if(false) {
    $dialects = dialectList();
    print_r($dialects);
  }

  // Get voices
  if(false) {
    $languageId = '61b8b2f54268666c126babc9'; // English
    $dialectId = '61b8b31c4268666c126bace7'; // United States

    $voices = voiceList($languageId, $dialectId);
    print_r($voices);
  }

  // Generate audio
  if(false) {
    $content = 'Hello, thank you for giving Fliki API a try!';
    $voiceId = '61b8b45a4268666c126bb32b'; // English, United States, Sara

    $audio = generateAudio($content, $voiceId);
    print_r($audio);
  }
})();
