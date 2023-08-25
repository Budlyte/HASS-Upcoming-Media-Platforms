Be sure to add the below to your configuration.yaml

  &ndash; platform: radarr_upcoming_media  
      api_key: !secret Radarr_Key  
      host: localhost  
      port: 7878  
      days: 7  
      ssl: false  
      max: 10  
And this to your UI-lovelace.yaml
&ndash; type: custom:upcoming-media-card
  entity: sensor.radarr_upcoming_media
  title: Upcoming Movies
