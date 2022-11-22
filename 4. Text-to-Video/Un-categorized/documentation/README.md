# API documentation
Your users can generate audio and video content with our AI-powered Fliki API. They can generate content in 75+ languages, 800+ voices and 100+ dialects!

## Pricing

| From | To | Total duration | Price per credit |
| --- | --- | --- | --- |
| 0 | 600 | 10 min | $0 |
| 600 | 10800 | 3 hours | $0.0035 |
| 10800 | 21600 | 6 hours | $0.003 |
| 21600 | ∞ | ∞ | $0.0025 |

Note: Your card will be billed for usage worth of every $50.

## API key
Head over to [Accounts → API](https://app.fliki.ai/account/api) section and get the API key.

## API endpoints

### Language list
Get list of languages
```bash
curl \
  -H "Authentication: Bearer <API KEY>" \
  -H "Content-Type: application/json" \
  -X GET https://api.fliki.ai/v1/languages
```

### Dialect list
Get list of dialects
```bash
curl \
  -H "Authentication: Bearer <API KEY>" \
  -H "Content-Type: application/json" \
  -X GET https://api.fliki.ai/v1/dialects
```

### Voice list
Get list of voices (along with supported voice styles) by language (required) and dialect (required)
```bash
curl \
  -H "Authentication: Bearer <API KEY>" \
  -H "Content-Type: application/json" \
  -d '{"languageId": "<LANUGAGE ID>", "dialectId": "<DIALECT ID>"}' \
  -X POST https://api.fliki.ai/v1/voices
```

### Generate audio
Generate audio for given content (plain text or SSML, required), voice (required) and voiceStyle (optional)
```bash
curl \
  -H "Authentication: Bearer <API KEY>" \
  -H "Content-Type: application/json" \
  -d '{"content": "<CONTENT>", "voiceId": "<VOICE ID>", "voiceStyleId": "<VOICE STYLE ID>"}' \
  -X POST https://api.fliki.ai/v1/generate/audio
```
Note: The file generated are hosted on Fliki's storage server and is deleted automatically after one month. We expect you to copy it to your own storage server for long term availability.

### Usage
Get usage for current billing period
```bash
curl \
  -H "Authentication: Bearer <API KEY>" \
  -H "Content-Type: application/json" \
  -X GET https://api.fliki.ai/v1/usage
```
