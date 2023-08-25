Be sure to add the below to your configuration.yaml

  &ndash; platform: sonarr_upcoming_media  
      api_key: !secret Sonarr_Key  
      host: localhost  
      port: 8787  
      days: 7  
      ssl: false  
      max: 10  

      
And this to your UI-lovelace.yaml  

&ndash; type: custom:upcoming-media-card  
  entity: sensor.sonarr_upcoming_media  
  title: Upcoming Shows  
