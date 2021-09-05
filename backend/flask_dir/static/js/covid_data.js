function change_dates(dates) {

  $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: "/covid/change_dates",
    data: JSON.stringify(dates),
    success: function (data) {
      if (data.status === "OK") {
          load_data();

      } else {
        console.log("error");
        window.location.assign('/');
      }
    },
    dataType: "json",
  });
}

function change_country(country, type) {
  $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: "/covid/" + type,
    data: JSON.stringify(country),
    success: function (data) {
      if (data.status === "OK") {

        load_data();

        setTimeout(function () {
          $("#country_input").removeClass("is-valid");
        }, 500);
        document.getElementById("country_input").value = "";
      } else {
        console.log("error");
        setTimeout(function () {
          $("#country_input").removeClass("is-valid");
          $("#country_input").addClass("is-invalid");
        }, 500);
      }
    },
    dataType: "json",
  });
}

function round_num(num, decimal) {
  if (num) {
    return num.toFixed(decimal);
  }
  return num;
}

function addComma(x, symbol = null) {
  if (x) {
      const fixed = round_num(x, 2)
          .toString()
          .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      if (symbol) {
      fixed + symbol;
    }
    return fixed;
  }
  return x;
}

function load_data(){
    var req1 = new Promise(function(resolve, reject) {
        setTimeout(function() { resolve(get_our_world());reject(console.log('our world failed')) }, 1000);
        });

    var req2 = new Promise(function(resolve, reject) {
        setTimeout(function() { resolve(get_daily());reject(console.log('john failed')) }, 2000);
        });

    var req3 = new Promise(function(resolve, reject) {
        setTimeout(function() { resolve(get_our_world_tests()); reject(console.log('tests failed'))}, 3000);
        });

    Promise.race([req1, req2, req3]).then(function(results) {
        console.log(results);
    }).catch(function(one, two, three) {
        console.log('Catch: ', one,two,three);
    });
}


function get_daily() {
  fetch("/covid/get_daily")
    .then(function (response) {
      return response.json();
    }).catch((e)=> {return e})
    .then(function (data) {
      render_daily(data);
      return '200'
    }).catch((e)=> {return e});
}

function get_our_world_tests() {
  fetch("/covid/get_our_world_tests")
    .then(function (response) {
      return response.json();
    }).catch((e)=> {return e})
    .then(function (data) {
      render_our_world_tests(data);
      return '200';
    }).catch((e)=> {return e});
}

function get_our_world() {
  fetch("/covid/get_our_world")
    .then(function (response) {
      return response.json();
    }).catch((e)=> {return e})
    .then(function (text) {
      $("#total_cases_per_million").text(
        addComma(text["World"]["total_cases_per_million"])
      );
      $("#total_deaths_per_million").text(
        addComma(text["World"]["total_deaths_per_million"])
      );
      $("#total_vaccinations").text(
        addComma(text["World"]["total_vaccinations"])
      );
      $("#total_vaccinations_per_hundred").text(
        addComma(text["World"]["total_vaccinations_per_hundred"], "%")
      );
      render_our_world(text, Object.keys(text));
      return '200';
    }).catch((e)=> {return e});
}

function change_border_color(color) {
  return color.replace(
    /rgba?(\(\s*\d+\s*,\s*\d+\s*,\s*\d+)(?:\s*,.+?)?\)/,
    "rgba$1,1)"
  );
}

function line_dataset(key, data_spec, color, data_info) {
  return {
    label: key + data_info,
    fill: false,
    borderColor: color[0],
    pointHighlightStroke: "rgba(220,220,220,1)",
    data: data_spec,
    type: "line",
    order: 1,
    hoverBackgroundColor: color[1],
  };
}

function bar_dataset(key, data_spec, color, data_info) {
  return {
    label: key + data_info,
    backgroundColor: color[1],
    pointHighlightStroke: "rgba(220,220,220,1)",
    data: data_spec,
    order: 2,
    hoverBackgroundColor: color[1],
    borderColor: change_border_color(color[1]),
    borderWidth: 1,
  };
}

function render_daily(data) {
    const mixed_dataset = [];
    let country_butt = "";

    $("#from_date").val(data["date_range"]["from"]);
  $("#to_date").val(data["date_range"]["to"]);

  Object.keys(data["cases"]).forEach(function (key) {
    country_butt +=
      '<button class="btn btn-outline-danger border rounded-pill" style="color:' +
      data["color"][key][0] +
      ';margin-left: 2%" data-toggle="tooltip" type="button" name="remove_country" title="Remove Country" onclick="change_country(this.id,this.name)" id="' +
      key +
      '">' +
      key +
      "</button>";
    mixed_dataset.push(
      line_dataset(key, data["cases"][key], data["color"][key], ' Cases'),
      bar_dataset(key, data["deaths"][key], data["color"][key], ' Deaths')
    );
  });
  document.getElementById("line_chart_loader").innerHTML =
    '<canvas id="line-chart" style="width: 100%; height: 100%;"></canvas>';
  document.getElementById("country_but").innerHTML = country_butt;

  new Chart(document.getElementById("line-chart"), {
    type: "bar",
    data: {
      datasets: mixed_dataset,
      labels: data.dates,
    },
    options: {
      legend: { labels: { fontColor: "grey" } },
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

function render_our_world_tests(data) {
    const test_mixed_data = [];

    Object.keys(data["daily_change_total_thousand"]).forEach(function (key) {
    test_mixed_data.push(
      line_dataset(key, data["short_term_tests_per_case"][key], data["color"][key], ' Tests per Case'),
      bar_dataset(key,  data["daily_change_total_thousand"][key], data["color"][key], ' Daily Change in tests per Thousand')
    );
  });

  document.getElementById("tests_line_chart").innerHTML =
    '<canvas id="tests_line" style="width: 100%; height: 100%;"></canvas>';
  new Chart(document.getElementById("tests_line"), {
    type: "bar",

    data: {
      labels: data.dates,
      datasets: test_mixed_data,
    },
    options: {
      legend: { labels: { fontColor: "grey" } },
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

//For Our World In data Graphs
function render_our_world(data, labels) {
  //For Bar Chart
  const cases_mil = [];
  const deaths_mil = [];
  const gdp_per_capita = [];

  //For Horizontal
    const people_fully_vaccinated_per_hundred = [];
    const people_vaccinated_per_hundred = [];
    const extreme_poverty = [];

    delete data["World"];
  labels.pop();
  fill_world(data);

  Object.keys(data).forEach(function (key) {
    //For Bar Chart
    cases_mil.push(round_num(data[key]["total_cases_per_million"], 2));
    deaths_mil.push(round_num(data[key]["total_deaths_per_million"], 2));
    gdp_per_capita.push(round_num(data[key]["gdp_per_capita"], 2));
    //For Horizontal Bar Chart
    people_fully_vaccinated_per_hundred.push(
      data[key]["people_fully_vaccinated_per_hundred"]
    );
    people_vaccinated_per_hundred.push(
      data[key]["people_vaccinated_per_hundred"]
    );
    extreme_poverty.push(data[key]["extreme_poverty"]);
  });

  document.getElementById("bar_chart_area").innerHTML =
    '<canvas id="bar-chart-grouped" style="width: 100%; height: 100%;"></canvas>';
  new Chart(document.getElementById("bar-chart-grouped"), {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Cases Per Million",
          backgroundColor: "#4e73df",
          data: cases_mil,
        },
        {
          label: "Total Deaths Per Million",
          backgroundColor: "#D9534F",
          data: deaths_mil,
        },
        {
          label: "GDP Per capita",
          backgroundColor: "#f0ad4e",
          data: gdp_per_capita,
        },
      ],
    },
    options: {
      legend: { labels: { fontColor: "grey" } },
      responsive: true,
      maintainAspectRatio: false,
    },
  });

  document.getElementById("bar_chart_area_horiz").innerHTML =
    '<canvas id="bar-chart-horizontal" style="width: 100%; height: 100%;"></canvas>';
  new Chart(document.getElementById("bar-chart-horizontal"), {
    type: "horizontalBar",
    axisY: {
      valueFormatString: "$#,###,#0",
    },

    data: {
      labels: labels,
      datasets: [
        {
          label: "People Fully Vaccinated Percent",
          backgroundColor: "#5cb85c",
          data: people_fully_vaccinated_per_hundred,
        },
        {
          label: "People Vaccinated Percent",
          backgroundColor: "#f0ad4e",
          data: people_vaccinated_per_hundred,
        },
        {
          label: "Extreme Poverty",
          backgroundColor: "#D9534F",
          data: extreme_poverty,
        },
      ],
    },
    options: {
      legend: { display: true, labels: { fontColor: "grey" } },
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

function fill_world(data) {
    let tbody = "";
    jQuery("#table_spinner").fadeOut(10);
  for (let value in data) {
    tbody += `<tr>
        <td>${value}</td>
        <td>${addComma(data[value]["hospital_beds_per_thousand"])}</td>
        <td>${addComma(data[value]["aged_70_older"])}</td>
        <td>${addComma(data[value]["median_age"])}</td>
        <td>${addComma(data[value]["population"])}</td>
        </tr>`;
  }
  tbody += "";
  document.getElementById("tbody_world_data_info").innerHTML = tbody;
}
