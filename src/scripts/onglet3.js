import * as preproc from './preprocess.js'

export function build(div) {
  buildHeatmap(div)
}

// https://d3-graph-gallery.com/heatmap.html
function buildHeatmap(div) {
  // TODO : adapt to div size

  // set the dimensions and margins of the graph
  const margin = {top: 30, right: 0, bottom: 70, left: 120},
    width = 500 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  // append the svg object to the body of the page
  const svg = div.select("#tab-3-heatmap")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)

  // Labels of row and columns
  const myGroups = preproc.GLOBAL_VESSEL_TYPE
  const myVars = preproc.REGION_NAME

  // Build X scales and axis:
  const x = d3.scaleBand()
    .range([ 0, width ])
    .domain(myGroups)
    .padding(0.01)

  svg.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x))
    .selectAll('text')
    .attr('transform', 'translate(-20,20)rotate(-45)')

  // Build Y scales and axis:
  const y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(myVars)
    .padding(0.01)
  svg.append("g")
    .call(d3.axisLeft(y))

  // Build color scale
  const myColor = d3.scaleLinear()
    .range(["white", "#ff0000"])
    .domain([1,72375]) //maximum hardocodé sur la valeur max


function transformData(d) {
  let map = new Map();
  //const dateStart = new 
  //const dateStop = 
  d.forEach(line => {
    const keyStart = line['Arrival Region']+line['Global Vessel Type'];//line['Arrival Date']+line['Arrival Region']+line['Global Vessel Type'];
    const keyStop = line['Departure Region']+line['Global Vessel Type'];//line['Departure Date']+line['Departure Region']+line['Global Vessel Type'];
    if (!map.has(keyStart)) {
      map.set(keyStart, {
        //'Date': line['Arrival Date'],
        'Region': line['Arrival Region'].slice(0,-7),
        'Type': line['Global Vessel Type'],
        'count': 1
        });
    } else {
      const current = map.get(keyStart);
      current.count += 1;
      map.set(keyStart, current);
    }
    if (!map.has(keyStop)) {
      map.set(keyStop, {
        //'Date': line['Departure Date'],
        'Region': line['Departure Region'].slice(0,-7),
        'Type': line['Global Vessel Type'],
        'count': 1
        });
    } else {
      const current = map.get(keyStop);
      current.count += 1;
      map.set(keyStop, current);
    }
  })
  return Array.from(map.values())
}

  //Read the data
  d3.csv("./TRIP_HEATMAP.csv").then( function(data) { //"https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/heatmap_data.csv"
    // add the squares and interaction
    const transformedData = transformData(data)
    svg.selectAll()
    .data(transformedData, function(d) {
      return d.Type+':'+d.Region;
    })
    .enter()
    .append("g")
    .attr("class", "square")
    .on('mouseenter', function() { rectSelect(this, x, y) })
    .on('mouseleave', function() { rectUnselect(this) })
    .append("rect")
      .attr("x", function(d) { return x(d.Type) })
      .attr("y", function(d) { return y(d.Region) })
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { return myColor(d.count) })
  })
}

function rectSelect(element, x, y) {
  d3.select(element)
    .append("text")
    .attr('x', function(d) { return x(d.Type) + x.bandwidth() / 2; })
    .attr('y', function(d) { return y(d.Region) + y.bandwidth() / 2; })
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'middle')
    .text(function(d) {
      return d.count
    })
}

function rectUnselect(element) {
  d3.select(element)
    .select('text')
    .remove()
}
