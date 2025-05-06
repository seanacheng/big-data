val file1 = sc.textFile("/h/scheng02/BigData/Quiz_5/2024_06.asc")
val file2 = sc.textFile("/h/scheng02/BigData/Quiz_5/2024_07.asc")

val file1Split = file1.map(line => line.split("\\|"))
val file2Split = file2.map(line => line.split("\\|"))

val combinedRDD = file1Split.union(file2Split)

val airlineDelayRDD = combinedRDD.map(line => (line(0), line(21).toInt)).filter { case (_, delay) => delay >= 0 }

val airlineDelaySumCountRDD = airlineDelayRDD.mapValues(delay => (delay, 1)).reduceByKey { case ((sum1, count1), (sum2, count2)) => (sum1 + sum2, count1 + count2) }

val airlineAvgDelayRDD = airlineDelaySumCountRDD.mapValues { case (totalDelay, totalCount) => totalDelay.toDouble / totalCount }

val airlineNameMap = Map(
  "DL" -> "Delta Airlines",
  "AA" -> "American Airlines",
  "UA" -> "United Airlines",
  "WN" -> "Southwest Airlines",
  "B6" -> "JetBlue Airways",
  "AS" -> "Alaska Airlines",
  "NK" -> "Spirit Airlines",
  "F9" -> "Frontier Airlines",
  "HA" -> "Hawaiian Airlines",
  "G4" -> "Allegiant Air"
)
val sortedAirlineByNameAvgDelayRDD = airlineAvgDelayRDD.map { case (airlineCode, avgDelay) => (airlineNameMap.getOrElse(airlineCode, airlineCode), avgDelay) }.sortBy(_._2, ascending = true)

sortedAirlineByNameAvgDelayRDD.collect().foreach { case (airline, avgDelay) => println(s"$airline\t$avgDelay") }



val departureTimeDelayRDD = combinedRDD.map(line => {
    val departureTime = line(10).toInt
    val delay = line(20).toInt
    
    val timeBlock = departureTime match {
      case t if (2200 <= t && t <= 2359) || (0 <= t && t <= 559)  => "night (10 pm - 6 am)"
      case t if 600 <= t && t <= 959                             => "morning (6 am to 10 am)"
      case t if 1000 <= t && t <= 1359                           => "mid-day (10 am to 2 pm)"
      case t if 1400 <= t && t <= 1759                           => "afternoon (2 pm - 6 pm)"
      case t if 1800 <= t && t <= 2159                           => "evening (6 pm - 10 pm)"
      case _ => "Unknown"
    }

    (timeBlock, delay)
  }).filter { case (_, delay) => delay >= 0 }

val departureTimeDelaySumCountRDD = departureTimeDelayRDD.mapValues(delay => (delay, 1)).reduceByKey { case ((sum1, count1), (sum2, count2)) => (sum1 + sum2, count1 + count2) }

val departureTimeAvgDelayRDD = departureTimeDelaySumCountRDD.mapValues { case (totalDelay, totalCount) => totalDelay.toDouble / totalCount }

departureTimeAvgDelayRDD.sortBy(_._2, ascending = true).collect().foreach { case (bucket, avgDelay) => println(s"$bucket\t$avgDelay") }



val airportDepartureDelayRDD = combinedRDD.map(line => (line(6), line(20).toInt)).filter { case (_, delay) => delay >= 0 }
val airportArrivalDelayRDD = combinedRDD.map(line => (line(7), line(21).toInt)).filter { case (_, delay) => delay >= 0 }
val combinedAirportDelayRDD = airportDepartureDelayRDD.union(airportArrivalDelayRDD)

val airportDelayCountRDD = combinedAirportDelayRDD.mapValues(delay => 1).reduceByKey { case (count1, count2) => count1 + count2 }

val airportNameMap = Map(
  "ATL" -> "Atlanta - Hartsfield Jackson",
  "BWI" -> "Baltimore/Wash. Int'l Thurgood.Marshall",
  "BOS" -> "Boston - Logan International",
  "CLT" -> "Charlotte - Douglas",
  "MDW" -> "Chicago - Midway",
  "ORD" -> "Chicago - O'Hare",
  "CVG" -> "Cincinnati Greater Cincinnati",
  "DFW" -> "Dallas-Fort Worth International",
  "DEN" -> "Denver - International",
  "DTW" -> "Detroit - Metro Wayne County",
  "FLL" -> "Fort Lauderdale Hollywood International",
  "IAH" -> "Houston - George Bush International",
  "LAS" -> "Las Vegas - McCarran International",
  "LAX" -> "Los Angeles International",
  "MIA" -> "Miami International",
  "MSP" -> "Minneapolis-St. Paul International",
  "EWR" -> "Newark Liberty International",
  "JFK" -> "New York - JFK International",
  "LGA" -> "New York - LaGuardia",
  "MCO" -> "Oakland International",
  "OAK" -> "Orlando International",
  "PHL" -> "Philadelphia International",
  "PHX" -> "Phoenix - Sky Harbor International",
  "PDX" -> "Portland International",
  "SLC" -> "Salt Lake City International",
  "STL" -> "St. Louis Lambert International",
  "SAN" -> "San Diego Intl. Lindbergh Field",
  "SFO" -> "San Francisco International",
  "SEA" -> "Seattle-Tacoma International",
  "TPA" -> "Tampa International",
  "DCA" -> "Washington - Reagan National",
  "IAD" -> "Washington - Dulles International"
)
val sortedAirportByNameDelayCountRDD = airportDelayCountRDD.map { case (airportCode, totalDelays) => (airportNameMap.getOrElse(airportCode, airportCode), totalDelays) }.sortBy(_._2, ascending = false)

sortedAirportByNameDelayCountRDD.collect().foreach { case (airport, totalDelays) => println(s"$airport\t$totalDelays") }

val airportDepartureRDD = combinedRDD.map(line => (line(6), 1))
val airportArrivalRDD = combinedRDD.map(line => (line(7), 1))
val airportFlightsCountRDD = airportDepartureRDD.union(airportArrivalRDD).reduceByKey { case (count1, count2) => count1 + count2 }

val sortedAirportByNameFlightsCountRDD = airportFlightsCountRDD.map { case (airportCode, totalFlights) => (airportNameMap.getOrElse(airportCode, airportCode), totalFlights) }.sortBy(_._2, ascending = false)

sortedAirportByNameFlightsCountRDD.collect().foreach { case (airport, totalFlights) => println(s"$airport\t$totalFlights") }
