Be sure to add the below to your configuration.yaml

  &ndash; platform: radarr_upcoming_media  
      api_key: !secret Radarr_Key  
      host: localhost  
      port: 7878  
      days: 7  
      ssl: false  
      max: 10  
