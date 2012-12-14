from django.http import HttpResponse
from pmap.models import ItemLocation
from django import template
from django.db.models import Sum

t_map = template.Template("""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Prescriptions (AP): Heatmap Layer</title>
    <link href="/maps/documentation/javascript/examples/default.css" rel="stylesheet">
    <script src="https://maps.googleapis.com/maps/api/js?sensor=false&libraries=visualization"></script>
    <script>
      // Adding 500 Data Points
      var map, pointarray, heatmap;

      var taxiData = [
{% for il in ils %}
{location: new google.maps.LatLng({{il.lat}},{{il.lon}}), weight: {{il.quantity}}},{% endfor %}
	];

      function initialize() {
        var mapOptions = {
          zoom: 6,
          center: new google.maps.LatLng(52.6, -1.4),
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        map = new google.maps.Map(document.getElementById('map_canvas'),
            mapOptions);

        pointArray = new google.maps.MVCArray(taxiData);

        heatmap = new google.maps.visualization.HeatmapLayer({
          data: pointArray,
          maxIntensity: 5,
          radius: 20
        });

        heatmap.setMap(map);
      }

      function toggleHeatmap() {
        heatmap.setMap(heatmap.getMap() ? null : map);
      }

      function changeGradient() {
        var gradient = [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(255, 0, 0, 1)'
        ]
        heatmap.setOptions({
          gradient: heatmap.get('gradient') ? null : gradient
        });
      }

      function changeIntensity() {
        heatmap.setOptions({maxIntensity: heatmap.get('maxIntensity') ? null : 150000});
      }

      function changeRadius() {
        heatmap.setOptions({radius: heatmap.get('radius') ? null : 35});
      }

      function changeOpacity() {
        heatmap.setOptions({opacity: heatmap.get('opacity') ? null : 0.2});
      }
    </script>
  </head>

  <body onload="initialize()">
    <div id="map_canvas" style="height: 600px; width: 800px;"></div>
    <button onclick="toggleHeatmap()">Toggle Heatmap</button>
    <button onclick="changeGradient()">Change gradient</button>
    <button onclick="changeRadius()">Change radius</button>
    <button onclick="changeOpacity()">Change opacity</button>
    <button onclick="changeIntensity()">Change intensity</button>
  </body>
</html>
""")

t_home = template.Template("""
<head>
    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/css/bootstrap-combined.min.css" rel="stylesheet">
</head>
<table>
{% for il in ils %}
<tr>
    <td>
    <a href="/map/{{il.item_id}}">
    {{il.item_name}}
    </a>
    </td><td>
    {{il.quantity__sum}}
    </td>
</tr>
{% endfor %}
</table>
""")

def home(request):
    c = template.Context()
    c['ils'] = ItemLocation.objects.values('item_id', 'item_name').annotate(Sum('quantity')).order_by('-quantity__sum')
    return HttpResponse(t_home.render(c))
    
def map(request, iid):
    c = template.Context()
    c['ils'] = ItemLocation.objects.all().filter(item_id=iid)
    return HttpResponse(t_map.render(c))
