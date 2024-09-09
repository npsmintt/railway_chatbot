-- CREATE DATABASE chatbot_contingency;
USE chatbot_contingency;

-- DROP TABLE blockage_contingency_plan;
-- DROP TABLE weather_contingency_plan;
-- DROP TABLE other_contingency_plan;

-- select * from blockage_contingency_plan;
-- select * from weather_contingency_plan;
-- select * from other_contingency_plan;

CREATE TABLE blockage_contingency_plan (
severity VARCHAR(20) NOT NULL,
location_a VARCHAR(30) NOT NULL,
location_b VARCHAR(30) NOT NULL,
controller_instructions TEXT NOT NULL,
resource_required TEXT NOT NULL,
infrastructure TEXT NOT NULL,
staff_deployment TEXT NOT NULL,
alternative_transport TEXT NOT NULL,
customer_message TEXT NOT NULL,
internal_message TEXT NOT NULL,
electronic_information TEXT NOT NULL,
CONSTRAINT PK_blockage_contingency_plan PRIMARY KEY (severity, location_a, location_b));

CREATE TABLE weather_contingency_plan (
weather VARCHAR(50) NOT NULL,
plan TEXT NOT NULL,
CONSTRAINT PK_weather_contingency_plan primary key (weather));

CREATE TABLE other_contingency_plan(
contingency varchar(100) NOT NULL,
plan TEXT NOT NULL,
CONSTRAINT PK_other_contingency_plan PRIMARY KEY (contingency));

INSERT INTO weather_contingency_plan
VALUES ("frost", "4.1. Frost is defined as the air temperature falling to zero degrees Celsius or below.
4.2. Risks with frost include arcing on the OHLE and frozen doors. In the case of the latter, depots and stabling points need to treat train doors before service. In the case of the former, the arcing is to be expected and should not be considered a concern.
4.3. Class 379 units are fitted with a Line Interference Monitor which identifies electrical interference caused by the operation of the train. In frost conditions arcing from the pantograph can cause the LIM to continually trip the VCB on the train. Class 379 units are fitted with an Ice Mode which raises the tolerance of the LIM and prevents tripping of the VCB. 
4.4. Ice Mode is initiated by the Driver and needs to be initiated each time the cab is activated. When the forecast air temperature is below 2 degrees the Duty Information Manager will post a notice on the depot Traincrew Information Monitors for those depots that operate Class 379 units, reminding drivers to activate ice mode between the times that the temperature is forecast to be below 2 degrees.
4.5. In the event of a frost risk being forecast, a Tyrell message will be emailed out along with a message placed on Whiteboard highlighting the affected areas. Stations in the affected areas will then be expected to enact the ‘Winterisation Plan’ as drawn up by the Customer Service team. The ‘Winterisation Plan’ is re-issued on an annual basis in November, having been reviewed in September. The thresholds for the ‘Winterisation Plan’ being enacted can be found within this plan.
");

INSERT INTO weather_contingency_plan 
VALUES ("snow", "5.1. Snow can have a huge impact on GA’s ability to deliver a train service. It has far-reaching effects ranging from damage to rolling stock and the infrastructure through to safety risks for our staff and customers on platforms, car parks and stairs.
5.2. If snow is forecast a company conference will be called to discuss the required mitigations and actions. Any agreed actions will be disseminated to the business via the company messaging service. Consideration will be given to enacting the company’s Emergency Plan should the snow event be prolonged (more than 48 hours), as well as instigating Gold Command within the AICC.
5.3. Network Rail’s Key Route Strategy prioritises routes and sections of lines throughout the Anglia Route where effort shall be directed during periods of heavy snow. Details shall be contained in the Network Rail produced Winter Working Arrangements along with information in relation to any additional resources that may be required. The GA Weather Related Service Management plans can be found on the Control page of the Intranet.
5.4. Class 317 and Class 321 traction motor damage mitigation
5.4.1 Where snow is falling or lying snow is being disturbed by the passage of trains, the company will impose a speed restriction of 60mph on these units. This restriction will be applied to protect the motors on these units from water ingress which can cause the motors to flashover and fail. The required speed restriction is dictated by representatives from the Fleet department and will be communicated to all traincrew via a notice in depot signing on points. 
5.5. In the event of a snow risk being forecast, a Tyrell message will be emailed out along with a message placed on Whiteboard highlighting the affected areas. Stations in the affected areas will then be expected to enact the ‘Winterisation Plan’ as drawn up by the Customer Service team. The ‘Winterisation Plan’ is re-issued on an annual basis in November, having been reviewed in September. The thresholds for the ‘Winterisation Plan’ being enacted can be found within this plan.");

INSERT INTO weather_contingency_plan 
VALUES ("high winds", "6.1. High wind forecasts are advised through the normal weather forecasting arrangements. This advice is given when wind speeds are forecast in excess of pre-determined values (mean and gust)
6.2. High wind speeds can cause damage to the overhead line equipment and bring the risk of collision with fallen trees and airborne detritus. To mitigate these risks Network Rail will impose speed restrictions if the forecast wind speeds exceed set limits. Details of the trigger speeds are contained within the Network Rail National Control Instructions 7.1. Any required speed restrictions will be advised via an EWAT conference and broadcast to drivers via the normal company channels. Plans will be made in advance for possible requirements for Blanket Speed Restrictions along the guidelines used by Network Rail shown in the table below. However, a Structured Expert Judgement (SEJ) may take precedent over the guidelines (for example on the Clacton and Walton-on-the-Naze branches because of the age of the Overhead Line Equipment) and can be predefined by the route");

INSERT INTO weather_contingency_plan 
VALUES ("high temperatures", "7.1. Overhead Line Equipment
7.1.1 High temperatures can cause sagging of the overhead line equipment which brings a risk of dewirement. Certain locations on the GE route require a reduction in speed if the forecast temperature exceeds set limits. Details of these trigger speeds are outlined below. Any required speed restrictions will be advised via a EWAT conference and broadcast to drivers either by notices in traincrew signing on points or via a GSM-R general broadcast.
7.2. Critical Rail Temperatures
7.2.1 At certain sites across the Anglia route the rail can also be susceptible to high temperatures and can be easily damaged if exposed to significant temperature. This can also be the case with certain types of engineering work. These Critical Rail Temperature (CRT) sites are recorded and monitored by Network Rail. Any required speed restrictions over CRT sites will be advised via an EWAT conference and broadcast to drivers either by notices in traincrew signing on points or via a GSM-R general broadcast.
7.3. Bottled water
7.3.1 If high temperatures are forecast, the customer services team will arrange for stocks of bottled water to be held for customers at principal staffed stations and in Loco Hauled Coaching Stock DVT vehicles. These arrangements will be confirmed during the company daily conference or special weather conference. A list of the principal staffed stations at which bottled water is kept can be found in Appendix B.
7.4. Air conditioned stock rescue and detrainment
7.4.1 If, during high temperatures, rolling stock with air conditioning (Class 170, Class 321 Renatus, Class 360, Class 379, Mk.II coaching stock hired from DRS and Mk.III coaching stock) becomes disabled and the air conditioning on board ceases to function, the rescue and detrainment of passengers must be a priority. SM 7.8 and SM20.9 cover Train Evacuation and Stranded Train Arrangements.");

INSERT INTO weather_contingency_plan 
VALUES ("autumn arrangements and low adhesion", "8.1. Advice of RHTT circuits/Weather Forecasts
8.1.1 Traincrew depots will be made aware of current weather conditions and whether RHTT circuits have been completed successfully or not, based on information received from the Control Autumn Manager. This information will be posted to the depot Traincrew Information Monitors.
8.2. Defective Locomotive Traction Motors in leaf-fall season
8.2.1 During the leaf fall season all Class 90 locomotives should, where possible, have four traction motors operational on the first 3 loco hauled services from Norwich. Where possible, this should also apply to the locomotive stabled at Ipswich used to form the first Up service to London Liverpool Street. Class 90 locomotives should not be allowed into service with less than three operational traction motors. GA may decide to retime Norwich services to provide additional time in the morning peak to allow for slipping caused by low rail adhesion.
8.3. Autumn Delay Attribution
8.3.1 Autumn delays will be based around the process in the delay attribution. Reasonable losses in key sections are agreed between Network Rail and the company. This will be provided before the start of each season along with attribution guidelines. AICC staff responsible for Level 1 TDA attribution must be vigilant to ensure this is correct.
8.4. Daily Autumn Teleconference
8.3.1 A daily Autumn teleconference will take place at 12:30 between Network Rail and the Anglia route TOCs to provide an update on the previous day’s events, current conditions, and actions to mitigate against the impact of leaf fall for the following 24 hours. This will have a rotating chair, alternating between Network Rail and GA, with GA participation from Control, Performance and Fleet Planning teams. A template for this conference call can be found at Appendix A.");

INSERT INTO weather_contingency_plan 
VALUES ("flooding", "9.1. Throughout the year, Network Rail will issue flood alerts as received from the Environment Agency. Flooding can be swift and unexpected and will inevitably cause disruption to services.
9.2. The following locations have been identified by Network Rail and GA, from previous experience, as being both likely to flood and having a high impact on our ability to provide a service:
- Bishops Stortford to Roydon (paralleling the River Lea and the Lea and Stort Navigation Canal)
- Stoke Newington
- Audley End
- Stansted Airport Tunnel
- Clapton
- Maryland
- Seven Kings
- Manor Park
- Brundall
9.3. The following locations have been identified by Network Rail and GA, from previous experience, as being prone to flooding following high tides and storm surge events, and will have a high impact on our ability to provide a service:
- Haddiscoe
- Lowestoft
- River Stour viaduct (Manningtree)
- Cattawade viaduct (Brantham)
- Wrabness/Parkeston
9.4. In the event of any flooding reports, cautioning will take place as required by the Rule Book. Additional restrictions may be required by the relevant Fleet Manager to prevent damage to roller bearings.");

INSERT INTO weather_contingency_plan 
VALUES ("high tides", "9.1. Throughout the year, Network Rail will issue flood alerts as received from the Environment Agency. Flooding can be swift and unexpected and will inevitably cause disruption to services.
9.2. The following locations have been identified by Network Rail and GA, from previous experience, as being both likely to flood and having a high impact on our ability to provide a service:
- Bishops Stortford to Roydon (paralleling the River Lea and the Lea and Stort Navigation Canal)
- Stoke Newington
- Audley End
- Stansted Airport Tunnel
- Clapton
- Maryland
- Seven Kings
- Manor Park
- Brundall
9.3. The following locations have been identified by Network Rail and GA, from previous experience, as being prone to flooding following high tides and storm surge events, and will have a high impact on our ability to provide a service:
- Haddiscoe
- Lowestoft
- River Stour viaduct (Manningtree)
- Cattawade viaduct (Brantham)
- Wrabness/Parkeston
9.4. In the event of any flooding reports, cautioning will take place as required by the Rule Book. Additional restrictions may be required by the relevant Fleet Manager to prevent damage to roller bearings.");

INSERT INTO blockage_contingency_plan
VALUES ('partial','Liverpool Street', 'Stratford', 'When diverting mains to electrics etc, priority should always be given to the TOC on the unaffected lines...eg GA for Issues on the electric 
lines & MTR for issues on the main lines. 
Where possible avoid crossing up and down line services over the same Jn’s i.e. if there is a main line blockage between Bethnal Green and 
Bow, up main services to cross back the mains at Wheler Street and down line service to cross to electrics at Bethnal Green West Jn. 
Sub lines not to be used for GE services', 'MOM’s or Maintenance staff at either end of the affected section where trains are crossing mains to electrics / electrics to mains to ensure that 
someone is on site should there be issues with pointwork.', 'Points: All points between Liverpool Street and Bethnal Green could have an impact on the implementation of this plan',
'. TfL Rail
• Dependant on delays ,CSL2 and line status to be declared by TFL control
• Dependant on delays, TFL Rail staff to follow TFL’s PIDD local delivery plan
• Dependant on delays, CAT Team to be deployed where necessary to assist staff and customers.
GREATER ANGLIA
• CSL2 mobilised East and West via on-call structure
• HQ staff support to Liverpool Street for evening peak
• RPIs and MTST support at Liverpool Street, Stratford and Shenfield
• Request Driver Manager to Liverpool Street, Stratford and Shenfield via On-Call Operations East
• Advise contingency plan on traincrew information monitors (TIM) ) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich
• Last shuttle train at Wickford must be held to connect with last down services for Southend
','London Buses via any reasonable route
London Underground via any reasonable route
Abellio Greater Anglia services between Liverpool Street and Shenfield
TfL rail services between Liverpool St and Shenfield
c2c services between Fenchurch Street and Southend Central via Upminster 
London Overground services via any reasonable route
London Overground services between Romford and Upminster
Great Northern services between Kings Cross and Cambridge / Ely (journey time 45 minutes to Cambridge, 65 minutes to Ely) for 
connections on Abellio Greater Anglia, Cross Country and East Midlands Trains services between Cambridge / Ely and Norwich. (Journey time 60 Minutes Ely-Norwich
• Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and Norwich.',
'TfL Rail
LIVERPOOL STREET TO STRATFORD
[delay reason] at [location]
Peak - There are currently Minor / Severe Delays operating on TFL Rail, this is due to (xxxx). An amended service is in operation between Stratford 
and Gidea Park calling at all stations expected until (xxxx)
Same vice versa.
Off Peak – There are currently minor / severe delays operating on TFL Rail, this is due to (xxxx). 
This disruption is expected to last until [expected end time].
Customers should use alternative routes from Fenchurch Street for c2c services, London Underground and Local Buses. Valid National Rail tickets 
will be accepted by London Buses, London Underground, DLR, London Overground, Abellio Greater Anglia and c2c services. 
Greater Anglia train services between Liverpool St and Shenfield are also affected. Please check Abelliogreateranglia.co.uk, tfl.gov.co.uk or 
nationalrail.co.uk for further information.
GREATER ANGLIA
Due to [delay reason] at [location]/between [location and location] some lines are blocked.
Train services to and from this station/through these stations may be cancelled, delayed by up to [xx] mins or revised. Disruption is expected until 
[expected end time].
This is affecting Abellio Greater Anglia train services [from/towards], [between, in both directions] Liverpool Street and Braintree, Chelmsford, 
Witham, Colchester, Colchester Town, Harwich, Southminster.
TfL Rail services from Liverpool Street to Shenfield are also affected. Please check tfl.gov.uk or nationalrail.co.uk for further information.
Customers could also use London Underground Central line services on which Abellio Greater Anglia tickets will be accepted.
Greater Anglia tickets will be accepted on:
London Buses and London Underground on reasonable routes. 
TfL Rail
c2c',
'Contingency Plan GE01 is in operation/ being implemented
With no/ the following amendments.
East bound freight to be held to be held Westbourne Rd Jn until a firm path has been identified……Speak with SSM Upminster to hold', 'Greater Anglia Service Update at xx:xx
Owing to a xxx between London and Stratford 1 of the 2 lines London-bound/Stratford-bound is currently closed. We expect the line to reopen at xxx 
/ the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train services to 
normal.
In order to reduce congestion to/from London Liverpool Street we are currently running a reduced train service to/from London Liverpool Street and 
expect this to continue until approximately xx:xx
London – Southend/Southminster services: We are running a normal/20 minute frequency service between London and Southend. A shuttle 
service is in operation between Wickford and Southminster and customers travelling to/from London to these stations should change at Wickford. 
To ease congestion on our services customers may use C2C services. 
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: Services which would normally run between 
London and Harwich are running between Colchester and Harwich in both directions. Customers wishing to travel to/from these stations should 
change at Colchester. We are running a slightly reduced service on all other routes and would like to apologise to customers for any overcrowding 
which occurs as a result. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.
MTR Crossrail Service Update xx:xx
Metro Services (London – Shenfield stopping services): We are currently running a ten-minute frequency service stopping at all stations 
between London and Shenfield in both directions. In order to assist customers in making their journey, Greater Anglia tickets are being accepted on 
London Underground and London bus services on all reasonable routes.
');


-- SELECT customer_message FROM blockage_contingency_plan WHERE location_a = 'London Liverpool Street' and location_b = 'Stratford';

INSERT INTO blockage_contingency_plan
VALUES ('partial','Stratford', 'Ilford', 'When diverting mains to electrics etc, priority should always be given to the TOC on the unaffected lines...eg GA for Issues on the electric
lines & MTR for issues on the main lines 
For those 2Wxx services running with reduced stops the principles are: Keep booked 2Wxx headcodes. This best for workload on 
signaller, controllers and customer service.
Down road - Trains running with reduced stops as per the plan - xx10, xx30, xx50 ex Liverpool St, Trains running all stations as booked 
xx00, xx20, xx40 ex Liverpool St.
Up road – Trains running with reduced stops as per the plan - xx04, xx24, xx44 ex Shenfield, Trains running all stations as booked xx14, 
xx34, xx54 ex Shenfield.
','MOM’s or Maintenance staff at either end of the affected section where trains are crossing mains to electrics / electrics to mains to ensure that
someone is on site should there be issues with pointwork.','Points: All points between Liverpool Street and Bethnal Green could have an impact on the implementation of this plan','. . TfL Rail
• Dependant on delays ,CSL2 and line status to be declared by TFL control
• Dependant on delays, TFL Rail staff to follow TFL’s PIDD local delivery plan
• Dependant on delays, CAT Team to be deployed where necessary to assist staff and customers.
GREATER ANGLIA
• CSL2 mobilised East and West via on-call structure
• HQ staff support to Liverpool Street for evening peak
• RPIs and MTST support at Liverpool Street, Stratford and Shenfield
• Request Driver Manager to Liverpool Street, Stratford and Shenfield via On-Call Operations East
• Advise contingency plan on traincrew information monitors (TIM) ) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich
• Last shuttle train at Wickford must be held to connect with last down services for Southend','London Buses via any reasonable route, including Buses 25 and 86 between Stratford and Ilford
London Underground via any reasonable route
Greater Anglia services between Liverpool Street and Shenfield
TfL Rail services between Liverpool St and Shenfield
c2c services between Fenchurch Street and Southend Central via Barking and Upminster 
London Overground services via any reasonable route
London Overground services between Romford and Upminster
Great Northern services between Kings Cross and Cambridge / Ely (journey time 45 minutes to Cambridge, 65 minutes to Ely) for connections on Abellio Greater Anglia, Cross Country and East Midlands Trains services between Cambridge / Ely and Norwich. (Journey time 
60 Minutes Ely-Norwich
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and Norwich.', 'STRATFORD TO ILFORD
[delay reason] at [location]
Peak - There are currently Minor / Severe Delays operating on TFL Rail, this is due to (xxxx). An amended service is in operation between Stratford 
and Gidea Park calling at all stations expected until (xxxx) 
Same vice versa.
Off Peak – There are currently minor / severe delays operating on TFL Rail, this is due to (xxxx).
Certain TFL Rail services will not call at Maryland, Forest Gate and Manor Park expected until (xxxx)
Same vice versa.
This disruption is expected to last until [expected end time].
Customers should use alternative routes from Fenchurch Street for c2c services, London Underground and Local Buses. Valid National Rail tickets 
will be accepted by London Buses, London Underground, DLR, London Overground, Abellio Greater Anglia and c2c services. 
Abellio Greater Anglia train services between Liverpool St and Shenfield are also affected. Please check Abelliogreateranglia.co.uk, tfl.gov.co.uk or 
nationalrail.co.uk for further information.
GREATER ANGLIA
Due to [delay reason] at [location]/between [location and location] some lines are blocked.
Train services to and from this station/through these stations may be cancelled, delayed by up to [xx] mins or revised. Disruption is expected until 
[expected end time].
This is affecting Greater Anglia train services [from/towards], [between, in both directions] Liverpool Street and Southend Victoria, Braintree, 
Chelmsford, Witham, Colchester, Colchester Town, Clacton, Harwich, Southminster, Ipswich and Norwich.
TfL Rail services from Liverpool Street to Shenfield are also affected. Please check tfl.gov.uk or nationalrail.co.uk for further information.
Customers are advised to use Tfl Rail services between Ilford and Shenfield although their rail services are also affected Please check tfl.gov.uk or 
nationalrail.co.uk for further information.
', 'Contingency Plan GE02 is in operation/ being implemented
with no/ the following variations.','Abellio Greater Anglia Service Update at xx:xx
Owing to a xxx between London and Stratford 1 of the 2 lines London-bound/Stratford-bound is currently closed. We expect the line to reopen at xxx
/ the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train services to
normal.
In order to reduce congestion to/from London Liverpool Street we are currently running a reduced train service to/from London Liverpool Street and
expect this to continue until approximately xx:xx
Metro Services (London – Shenfield stopping services): We are currently running a ten-minute frequency service stopping at all stations
between London and Shenfield in both directions. In order to assist customers in making their journey, Greater Anglia tickets are being accepted on
London Underground and London bus services on all reasonable routes.
London – Southend/Southminster services: We are running a normal/20 minute frequency service between London and Southend. A shuttle
service is in operation between Wickford and Southminster and customers travelling to/from London to these stations should change at Wickford.
To ease congestion on our services customers may use C2C services.
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: Services which would normally run between
London and Harwich are running between Colchester and Harwich in both directions. Customers wishing to travel to/from these stations should
change at Colchester. We are running a slightly reduced service on all other routes and would like to apologise to customers for any overcrowding
which occurs as a result.
All other Abellio Greater Anglia Routes: There is currently a good service running on all other routes.');

INSERT INTO blockage_contingency_plan
VALUES ("partial","Ilford","Gidea Park","When diverting mains to electrics etc, priority should always be given to the TOC on the unaffected lines...eg GA for Issues on the electric
lines & MTR for issues on the main lines
For those 2Wxx services running with reduced stops the principles are: Keep booked 2Wxx headcodes. This best for workload on 
signaller, controllers and customer service.
Signaller and Controller Instructions:
If EL’s are blocked east of Chadwell Heath and services are diverted DML, Crossrail would like to run additional services to Chadwell Heath where 
resources and capacity are available.", "MOM’s or Maintenance staff at either end of the affected section where trains are crossing mains to electrics / electrics to mains to ensure that 
someone is on site should there be issues with pointwork.","Points: All points between Liverpool Street and Stratford could have an impact on the implementation of this plan", "TfL Rail
• Dependant on delays ,CSL2 and line status to be declared by TFL control
• Dependant on delays, TFL Rail staff to follow TFL’s PIDD local delivery plan
• Dependant on delays, CAT Team to be deployed where necessary to assist staff and customers.
GREATER ANGLIA
• CSL2 mobilised East and West via on-call structure
• HQ staff support to Liverpool Street for evening peak
• RPIs and MTST support at Liverpool Street, Stratford and Shenfield
• Request Driver Manager to Liverpool Street, Stratford and Shenfield via On-Call Operations East
• Advise contingency plan on traincrew information monitors (TIM) ) in the following traincrew depots: Liverpool Street, Colchester, Clacton, 
Ilford, Southend, Ipswich and Norwich
• Last shuttle train at Wickford must be held to connect with last down services for Southend", "Gidea Park and Romford,
Routes 294,496 and 498 run from Harold Wood to Gidea Park and Romford, 
Route 498 runs from Brentwood to Harold Wood, Gidea Park and Romford,
London Underground via any reasonable route
Greater Anglia services between Liverpool Street and Shenfield
TfL Rail services between Liverpool St and Shenfield
c2c services between Fenchurch Street and Upminster 
London Overground services via any reasonable route
London Overground services between Romford and Upminster
Great Northern services between King's Cross and Cambridge / Ely (journey time 45 minutes to Cambridge, 65 minutes to Ely) for 
connections on Abellio Greater Anglia, Cross Country and East Midlands Trains services between Cambridge / Ely and Norwich. (Journey time 
60 Minutes Ely-Norwich
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and Norwich.",
"IlFORD TO GIDEA PARK
[delay reason] at [location]
Peak - There are currently Minor / Severe Delays operating on TFL Rail, this is due to (xxxx). 
Off Peak – There are currently minor / severe delays operating on TFL Rail, this is due to (xxxx).
[delay reason] at [location]
This disruption is expected to last until [expected end time].
Customers should use alternative routes from Fenchurch Street for c2c services, London Underground and Local Buses. Valid National Rail tickets 
will be accepted by London Buses, London Underground, DLR, London Overground, Greater Anglia and c2c services. 
Greater Anglia train services between Liverpool St and Shenfield are also affected. Please check Abelliogreateranglia.co.uk, tfl.gov.co.uk or 
nationalrail.co.uk for further information.
GREATER ANGLIA
Due to [delay reason] at [location]/between [location and location] some lines are blocked.
Train services to and from this station/through these stations may be cancelled, delayed by up to [xx] mins or revised. Disruption is expected until 
[expected end time].This is affecting Greater Anglia train services [from/towards], [between, in both directions] Liverpool Street and Southend Victoria, Braintree, 
Chelmsford, Witham, Colchester, Colchester Town, Clacton, Harwich, Southminster, Ipswich and Norwich.
TfL Rail services from Liverpool Street to Shenfield are also affected. Please check tfl.gov.uk or nationalrail.co.uk for further information.
Customers to and from Southend Victoria are advised to use c2c services between Fenchurch Street and Southend.
Customers to and from Ipswich and Norwich are advised to travel via Cambridge on Greater Anglia services from Liverpool Street or Great Northern 
services from Kings’s Cross.
And Cambridge
Greater Anglia tickets will be accepted on:
London Buses and London Underground on reasonable routes. 
TfL Rail
c2c
Great Northern
Journey times will be extended by up to [xx]mins.",
"Contingency Plan GE03 is in operation/ being implemented
with no/ the following variations.",
"Owing to a xxx between Gidea Park and Ilford 1 of the 2 lines London-bound/Shenfield-bound is currently closed. We expect the line to reopen at 
xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train 
services to normal.
In order to manage the reduced line capacity to/from London Liverpool Street we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Southend/Southminster services: We are running a normal/20 minute frequency service between London and Southend. A shuttle 
service is in operation between Wickford and Southminster and customers travelling to/from London to these stations should change at Wickford. 
To ease congestion on our services customers may use C2C services. 
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: Services which would normally run between 
London and Harwich are running between Colchester and Harwich in both directions. Customers wishing to travel to/from these stations should 
change at Colchester. We are running a slightly reduced service on all other routes and would like to apologise to customers for any overcrowding 
which occurs as a result. 
All other Greater Anglia Routes: There is currently a good service running on all other routes
MTR Crossrail Service Update at xx:xx
Metro Services (London – Shenfield stopping services): We are currently running a 10-minute frequency service calling in both directions 
Brentwood, Harold Wood, Gidea Park, Ilford Manor Park, Forest Gate, Maryland and Stratford. In order to assist customers in making their journey, 
Greater Anglia tickets are being accepted on London Underground and London bus services on all reasonable routes. Trains wil l not be calling at 
Seven Kings, Goodmayes, Chadwell Heath and Romford. Customers are advised to take TfL Bus Route 86 or 25 from either Romford, Ilford, or 
Stratford");

INSERT INTO blockage_contingency_plan 
VALUES ("partial","Gidea Park", "Shenfield", "When diverting mains to electrics etc, priority should always be given to the TOC on the unaffected lines...eg GA for Issues on the electric
lines & MTR for issues on the main lines","MOM’s or Maintenance staff capable of route setting to be moved / positioned at both Gidea Park and Shenfield to ensure that someone is on site 
should there be issues with pointwork"," All points between Stratford and Shenfield could have an impact on the implementation of this plan" ,". TfL Rail
• Dependant on delays ,CSL2 and line status to be declared by TFL control
• Dependant on delays, TFL Rail staff to follow TFL’s PIDD local delivery plan
• Dependant on delays, CAT Team to be deployed where necessary to assist staff and customers.
GREATER ANGLIA
• CSL2 mobilised East and West via on-call structure
• HQ staff support to Liverpool Street for evening peak
• RPIs and MTST support at Liverpool Street, Stratford and Shenfield
• Request Driver Manager to Liverpool Street, Stratford and Shenfield via On-Call Operations East
• Advise contingency plan on traincrew information monitors (TIM) ) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich
• Last shuttle train at Wickford must be held to connect with last down services for Southend","London Buses via any reasonable route including Routes 174, 294 496 and 498 run between Gidea Park and Romford,
Routes 294,496 and 498 run from Harold Wood to Gidea Park and Romford, 
Route 498 runs from Brentwood to Harold Wood, Gidea Park and Romford,
London Underground via any reasonable route
Greater Anglia services between Liverpool Street and Shenfield
TfL Rail services between Liverpool St and Shenfield
c2c services between Fenchurch Street and Southend Central via Upminster 
London Overground services via any reasonable route
London Overground services between Romford and Upminster
Great Northern services between King's Cross and Cambridge / Ely (journey time 45 minutes to Cambridge, 65 minutes to Ely) for 
connections on Greater Anglia, Cross Country and East Midlands Trains services between Cambridge / Ely and Norwich. (Journey time 60 Minutes Ely-Norwich
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and Norwich.
", "GIDEA PARK - SHENFIELD
[delay reason] at [location]
Peak - There are currently Minor / Severe Delays operating on TFL Rail, this is due to (xxxx). 
Three services per hour will call at all stations.
Six services per hour will call at all stations between Chadwell Heath / Gidea Park(dependant on the blockage location) and Liverpool Street 
expected until (xxxx)
Same vice versa. 
Off Peak – There are currently minor / severe delays operating on TFL Rail, this is due to (xxxx).
Three services per hour will call at all stations.
Three services per hour will call at all stations between Chadwell Heath / Gidea Park(dependant on the blockage location) and Liverpool Street 
expected until (xxxx)
[delay reason] at [location]
This disruption is expected to last until [expected end time].
Customers should use alternative routes from Fenchurch Street for c2c services, London Underground and Local Buses. Valid National Rail tickets 
will be accepted by London Buses, London Underground, DLR, London Overground, Abellio Greater Anglia and c2c services. 
Greater Anglia train services between Liverpool St and Shenfield are also affected. Please check Abelliogreateranglia.co.uk, tfl.gov.co.uk or 
nationalrail.co.uk for further information.
GREATER ANGLIA
Due to [delay reason] at [location]/between [location and location] some lines are blocked.
Train services to and from this station/through these stations may be cancelled, delayed by up to [xx] mins or revised. Disruption is expected until 
[expected end time].
This is affecting Greater Anglia train services [from/towards], [between, in both directions] Liverpool Street and Southend Victoria, Braintree, 
Chelmsford, Witham, Colchester, Colchester Town, Harwich, Southminster.
TfL Rail services from Liverpool Street to Shenfield are also affected. Please check tfl.gov.uk or nationalrail.co.uk for further information.
Customers to and from Southend Victoria are advised to use c2c services between Fenchurch Street and Southend.
Customers to and from Ipswich and Norwich are advised to travel via Cambridge on Greater Anglia services from Liverpool Street or Great Northern 
services from Kings’s Cross.
And Cambridge
Greater Anglia tickets will be accepted on:
London Buses and London Underground on reasonable routes. 
TfL Rail
c2c
Great Northern
Journey times will be extended by up to [xx]mins", "Contingency Plan GE04 is in operation/ being implemented
with no/ the following variations.","Greater Anglia Service Update at xx:xx
Owing to a xxx between Gidea Park and Shenfield 1 of the 2 lines London-bound/Shenfield-bound is currently closed. We expect the line to reopen 
at xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train 
services to normal.
In order to manage the reduced line capacity to/from London Liverpool Street we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Southend/Southminster services: We are running a normal/20 minute frequency service between London and Southend. A shuttle 
service is in operation between Wickford and Southminster and customers travelling to/from London to these stations should change at Wickford. 
To ease congestion on our services customers may use C2C services. 
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: Services which would normally run between 
London and Harwich are running between Colchester and Harwich in both directions. Customers wishing to travel to/from these stations should 
change at Colchester. We are running a slightly reduced service on all other routes and would like to apologise to customers for any overcrowding 
which occurs as a result. 
All other Greater Anglia Routes: There is currently a good service running on all other routes
MTR Crossrail Service Update at xx:xx
Metro Services (London – Shenfield stopping services): We are currently running a 20-minute frequency service stopping at all stations 
between London and Shenfield in both directions and a 20-minute frequency limited stop service between London and Shenfield in both directions 
calling at Gidea Park, Ilford and Stratford. In order to assist customers in making their journey, Greater Anglia tickets are being accepted on London 
Underground and London bus services on all reasonable routes. Customers are advised to take TfL Bus Route 86 or 25 from either Ilford or 
Stratford.
");

INSERT INTO blockage_contingency_plan
VALUES ("partial", "Shenfield", "Church Lane", "Witham - Braintree shuttle to be used where resources allow...consider splitting an 8 car unit from elsewhere to provide a 4 car for the shuttle.",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Shenfield and Church Lane or Church Lane and Chelmsford to 
ensure that someone is on site should there be issues with pointwork",
"Points Shenfield: 2272, 2282, 2284, 
Points Church Lane: 2347, 2348.
Points Chelmsford: 2349, 235
",
"CSL2 mobilised for North via on-call structure
Request Driver Managers to Liverpool Street and Colchester via On-Call Operations L1 South East and North
Advise Liverpool Street Duty Station Manager
RPIs and MTST support at Chelmsford
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich",
"Colchester Town customers advised to use local buses to/from Colchester. Note GA Tickets are not passed.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich)",
"Owing to a {xxx} between Ingatestone and Shenfield/ Ingatestone and Chelmsford. 1 of the 2 lines London-bound/Colchester-bound is currently 
closed 
Trains between Chelmsford and Shenfield are experiencing 20 minute delays and an amended train service is in place.",
"Contingency Plan GE05 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Ingatestone and Shenfield/ Ingatestone and Chelmsford 1 of the lines London-bound/Colchester-bound is currently closed. 
We expect the line to reopen at xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we 
are working to return train services to normal.
In order to manage the reduced line capacity to/from Shenfield and Chelmsford we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Services which would normally run between London and Braintree are running between Witham and Braintree in both directions. Customers wishing 
to travel to/from these stations should change at Witham. 
Services which would normally run between London and Colchester Town are suspended Customers wishing to travel to/from Colchester Town are 
advised to use local buses to Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes");

INSERT INTO blockage_contingency_plan
VALUES ("partial", "Church Lane", "Chelmsford", "Witham - Braintree shuttle to be used where resources allow...consider splitting an 8 car unit from elsewhere to provide a 4 car for the shuttle.",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Shenfield and Church Lane or Church Lane and Chelmsford to 
ensure that someone is on site should there be issues with pointwork",
"Points Shenfield: 2272, 2282, 2284, 
Points Church Lane: 2347, 2348.
Points Chelmsford: 2349, 235
",
"CSL2 mobilised for North via on-call structure
Request Driver Managers to Liverpool Street and Colchester via On-Call Operations L1 South East and North
Advise Liverpool Street Duty Station Manager
RPIs and MTST support at Chelmsford
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich",
"Colchester Town customers advised to use local buses to/from Colchester. Note GA Tickets are not passed.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich)",
"Owing to a {xxx} between Ingatestone and Shenfield/ Ingatestone and Chelmsford. 1 of the 2 lines London-bound/Colchester-bound is currently 
closed 
Trains between Chelmsford and Shenfield are experiencing 20 minute delays and an amended train service is in place.",
"Contingency Plan GE05 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Ingatestone and Shenfield/ Ingatestone and Chelmsford 1 of the lines London-bound/Colchester-bound is currently closed. 
We expect the line to reopen at xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we 
are working to return train services to normal.
In order to manage the reduced line capacity to/from Shenfield and Chelmsford we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Services which would normally run between London and Braintree are running between Witham and Braintree in both directions. Customers wishing 
to travel to/from these stations should change at Witham. 
Services which would normally run between London and Colchester Town are suspended Customers wishing to travel to/from Colchester Town are 
advised to use local buses to Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes");

INSERT INTO blockage_contingency_plan 
VALUES ("partial", "Chelmsford", "Brickhouse", "Priority to AM / PM Peak services over Bi-Di section.
Witham - Braintree shuttle to be used where resources allow...consider splitting an 8 car unit from elsewhere to provide a 4 car for the shuttle. ",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Chelmsford and Brickhouse to ensure that someone is on site 
should there be issues with pointwork.",
"Points Chelmsford: 2349, 2356
Points at Brickhouse: 2360, 236",
"CSL2 mobilised for North via on-call structure
Request Driver Manager to Liverpool Street and Colchester via On-Call Operations L1 South East and L1 North
Advise Liverpool Street Duty Station Manager
RPIs and MTST support at Chelmsford for peak
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich.
Customer staff deployment….If only 1 platform available, all staff to work open platform",
"Colchester Town customers advised to use local buses to/from Colchester. Note AGA Tickets are not passed.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).",
"Owing to a {xxx} between Hatfield Peveral and Chelmsford. 1 of the 2 lines London-bound/Colchester-bound is currently closed.
Trains between Chelmsford and Hatfield Peverel are experiencing 20 minute delays and an amended train service is in place.",
"Contingency Plan GE06 is in operation/ being implemented
with no/ the following variations.
Customer staff deployment….If only 1 platform available, all staff to work open platform",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Chelmsford and Hatfield Peverel 1 of the lines London-bound/Colchester-bound is currently closed. We expect the line to 
reopen at xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return 
train services to normal.
In order to manage the reduced line capacity to/from Colchester and Chelmsford we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Services which would normally run between London and Braintree are running between Witham and Braintree in both directions. Customers wishing 
to travel to/from these stations should change at Witham. 
Services which would normally run between London and Colchester Town are suspended Customers wishing to travel to/from Colchester Town are 
advised to use local buses to Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes");

INSERT INTO blockage_contingency_plan
VALUES ("partial", "Brickhouse", "Witham",
"Priority to AM / PM Peak services over Bi-Di section.
Witham - Braintree shuttle to be used where resources allow...consider splitting an 8 car unit from elsewhere to provide a 4 car for the shuttle. ",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Brickhouse and Witham to ensure that someone is on site should 
there be issues with pointwork.",
"Points at Brickhouse: 2360, 2361
Points at Witham: 2367, 236",
"CSL2 mobilised for North via on-call structure
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Request Driver Manager to Liverpool Street and Colchester via On-Call Operations L1 South East and L1 North
Advise Liverpool Street Duty Station Manager
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich
",
"Colchester Town customers advised to use local buses to/from Colchester. Note GA Tickets are not passed.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich)",
"Owing to a {xxx} between Chelmsford and Witham. 1 of the 2 lines London-bound/Colchester-bound is currently closed.
Trains between Chelmsford and Witham are experiencing 20 minute delays and an amended train service is in place.",
"Contingency Plan GE07 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Chelmsford and Witham 1 of the lines London-bound/Colchester-bound is currently closed. We expect the line to reopen at 
xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train 
services to normal.
In order to manage the reduced line capacity to/from Colchester and Chelmsford we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Services which would normally run between London and Braintree are running between Witham and Braintree in both directions. Customers wishing 
to travel to/from these stations should change at Witham. 
Services which would normally run between London and Colchester Town are suspended Customers wishing to travel to/from Colchester Town are 
advised to use local buses to Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan 
VALUES ("partial", "Witham", "Kelvedon",
"“Flighting” of trains is preferable to ensure as many trains through the sections as possible.
",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Witham and Kelvedon / Kelvedon and Marks Tey / Marks Tey and 
Colchester to ensure that someone is on site should there be issues with pointwork.",
"Points at Witham: 2367, 2368
Points at Kelvedon: 2384, 2387
Points at Marks Tey: 2389, 2392
Points at Colchester: 3009, 301
",
"CSL2 mobilised for North via on-call structure
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Advise Liverpool Street Duty Station Manager
Request Octagon staff to attend Colchester Town (when booked unmanned)
RPIs/ MTST staff request to assist at Colchester and for AM peak
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Ipswich and Norwich
",
"Colchester Town customers advised to use local buses to/from Colchester. Note GA Tickets are not passed.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich)
",
"Owing to a {xxx} Witham and Kelvedon/ Kelvedon and Marks Tey/ Marks Tey and Colchester. Trains between Colchester and Witham are 
experiencing 20 minute delays and an amended train service is in place",
"Contingency Plan GE08 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Colchester and Witham 1 of the lines London-bound/Colchester-bound is currently closed. We expect the line to reopen at 
xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train 
services to normal
In order to manage the reduced line capacity to/from Colchester and Witham we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Services to and from Colchester Town are suspended. Customers wishing to travel to/from Colchester Town are advised to use local buses to 
Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan 
VALUES ("partial", "Kelvedon", "Marks Tey",
"“Flighting” of trains is preferable to ensure as many trains through the sections as possible.
",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Witham and Kelvedon / Kelvedon and Marks Tey / Marks Tey and 
Colchester to ensure that someone is on site should there be issues with pointwork.",
"Points at Witham: 2367, 2368
Points at Kelvedon: 2384, 2387
Points at Marks Tey: 2389, 2392
Points at Colchester: 3009, 301
",
"CSL2 mobilised for North via on-call structure
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Advise Liverpool Street Duty Station Manager
Request Octagon staff to attend Colchester Town (when booked unmanned)
RPIs/ MTST staff request to assist at Colchester and for AM peak
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Ipswich and Norwich
",
"Colchester Town customers advised to use local buses to/from Colchester. Note GA Tickets are not passed.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich)
",
"Owing to a {xxx} Witham and Kelvedon/ Kelvedon and Marks Tey/ Marks Tey and Colchester. Trains between Colchester and Witham are 
experiencing 20 minute delays and an amended train service is in place",
"Contingency Plan GE08 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Colchester and Witham 1 of the lines London-bound/Colchester-bound is currently closed. We expect the line to reopen at 
xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train 
services to normal
In order to manage the reduced line capacity to/from Colchester and Witham we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Services to and from Colchester Town are suspended. Customers wishing to travel to/from Colchester Town are advised to use local buses to 
Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan 
VALUES ("partial", "Marks Tey", "Colchester",
"“Flighting” of trains is preferable to ensure as many trains through the sections as possible.
",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Witham and Kelvedon / Kelvedon and Marks Tey / Marks Tey and 
Colchester to ensure that someone is on site should there be issues with pointwork.",
"Points at Witham: 2367, 2368
Points at Kelvedon: 2384, 2387
Points at Marks Tey: 2389, 2392
Points at Colchester: 3009, 301
",
"CSL2 mobilised for North via on-call structure
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Advise Liverpool Street Duty Station Manager
Request Octagon staff to attend Colchester Town (when booked unmanned)
RPIs/ MTST staff request to assist at Colchester and for AM peak
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Ipswich and Norwich
",
"Colchester Town customers advised to use local buses to/from Colchester. Note GA Tickets are not passed.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich)
",
"Owing to a {xxx} Witham and Kelvedon/ Kelvedon and Marks Tey/ Marks Tey and Colchester. Trains between Colchester and Witham are 
experiencing 20 minute delays and an amended train service is in place",
"Contingency Plan GE08 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Colchester and Witham 1 of the lines London-bound/Colchester-bound is currently closed. We expect the line to reopen at 
xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train 
services to normal
In order to manage the reduced line capacity to/from Colchester and Witham we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Services to and from Colchester Town are suspended. Customers wishing to travel to/from Colchester Town are advised to use local buses to 
Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan 
VALUES ("partial", "Colchester", "Manningtree", "GriffinWharf may be blocked
'Flighting' of triains is preferable to ensure as many trains through the sections as possible.",
"Colchester – Manningtree:
 Pilotman
Handsignaller
Barrier Operator for Ardleigh CCTV
Barrier Operator for Manningtree CCTV (if SLW over the Down Main)
Manningtree – Halifax Jn: 
 Pilotman
Handsignaller",
"Points at Colchester: 3025, 3029, 3034
Points at Manningtree: 1247, 1253, 1261, 1262
Points at Halifax Jn: 1301, 130
",
"CSL2 mobilised for North via on-call structure
Request Driver Manager to Colchester via On-Call Operations L1 North
Advise Liverpool Street Duty Station Manager
Request RPI assistance to aid transfer of passengers to Harwich shuttle;
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ipswich 
and Norwich",
"Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Peak: Special service to operate COL-LST calling at all stations to CHM and then SNF and SRA in place of 1Yxx services.
Off-Peak: None – train service operates as revised.
",
"Owing to a {xxx} between Colchester and Manningtree/Ipswich and Manningtree , trains between Colchester and Ipswich are experiencing 20 
minute delays and an amended train service is in place.
",
"Contingency Plan GE9 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Colchester and Manningtree/Ipswich and Manningtree ,1 of the lines Colchester-bound/Ipswich-bound is currently closed.
We expect the line to reopen at xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we 
are working to return train services to normal
In order to manage the reduced line capacity to/from Colchester and Ipswich we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Harwich, Ipswich and Norwich: 
Services which would normally run between London and Harwich are running between Maningtree and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Manningtree. 
Services which would normally run between London and Colchester Town are suspended Customers wishing to travel to/from Colchester Town are 
advised to use local buses to Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan 
VALUES ("partial", "Manningtree", "Halifax Junction", "GriffinWharf may be blocked
, 'Flighting' of triains is preferable to ensure as many trains through the sections as possible.",
"Colchester – Manningtree:
 Pilotman
Handsignaller
Barrier Operator for Ardleigh CCTV
Barrier Operator for Manningtree CCTV (if SLW over the Down Main)
Manningtree – Halifax Jn: 
 Pilotman
Handsignaller",
"Points at Colchester: 3025, 3029, 3034
Points at Manningtree: 1247, 1253, 1261, 1262
Points at Halifax Jn: 1301, 130
",
"CSL2 mobilised for North via on-call structure
Request Driver Manager to Colchester via On-Call Operations L1 North
Advise Liverpool Street Duty Station Manager
Request RPI assistance to aid transfer of passengers to Harwich shuttle;
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ipswich 
and Norwich",
"Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Peak: Special service to operate COL-LST calling at all stations to CHM and then SNF and SRA in place of 1Yxx services.
Off-Peak: None – train service operates as revised.
",
"Owing to a {xxx} between Colchester and Manningtree/Ipswich and Manningtree , trains between Colchester and Ipswich are experiencing 20 
minute delays and an amended train service is in place.
",
"Contingency Plan GE9 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Colchester and Manningtree/Ipswich and Manningtree ,1 of the lines Colchester-bound/Ipswich-bound is currently closed.
We expect the line to reopen at xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we 
are working to return train services to normal
In order to manage the reduced line capacity to/from Colchester and Ipswich we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Harwich, Ipswich and Norwich: 
Services which would normally run between London and Harwich are running between Maningtree and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Manningtree. 
Services which would normally run between London and Colchester Town are suspended Customers wishing to travel to/from Colchester Town are 
advised to use local buses to Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("partial", "Halifax Junction", "Ipswich", "Consider extending services through to Manningtree / ECS to Mistley and return for PM peak & Off peak also where possible.",
"Ipswich MOM to be stationed at Halifax Jn
During AM peak Colchester MOM to be stationed at Manningtree",
"Points: 1301, 1302, 1312, 1326, 1341, 1343",
"CSL2 mobilised for North via on-call structure
Request Driver Manager to Colchester via On-Call Operations L1 North
Advise Liverpool Street Duty Station Manager
Request RPI assistance to Ipswich.
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ipswich 
and Norwich",
"dvance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Peak: Special service to operate COL-LST calling at all stations to CHM and then SNF and SRA in place of 1Yxx services.
Off-Peak: None – train service operates as revised.",
"Owing to a {xxx} between Manningtree and Ipswich trains between Colchester and Ipswich are experiencing 20 minute delays and an amended 
train service is in place.",
"Contingency Plan GE10 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Colchester and Manningtree/Ipswich and Manningtree , one of the lines Colchester-bound/Ipswich-bound is currently 
closed. We expect the line to reopen at xxx / the line is currently closed and we are working to assess the problem / The line has now reopened 
and we are working to return train services to normal.
In order to manage the reduced line capacity to/from Colchester and Ipswich we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Ipswich and Norwich: 
Services which would normally run between London and Ipswich and Norwich are running with delays/ at a reduced frequency between Maningtree 
and Ipswich. Customers should allow additional time for their journeys. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("partial", "Ipswich", "East Suffolk Junction", "All 1Pxx services stop addl Stowmarket
If 2Wxx term stowmarket…bus service Ipswich-Needham Mkt-Stowmarket", "MOM’s or Maintenance staff capable of route setting to be moved / positioned Ipswich to ensure that someone is on site should there be issues with 
pointwork.",
"Points: 1341, 1326, 1364",
"CSL2 mobilised for North via on-call structure.
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Ipswich and 
Norwich.
All 1Pxx services stop addl Stowmarket
If 2Wxx term stowmarket…bus service Ipswich-Needham Mkt-Stowmarket",
"Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich). Or
Norwich customers to/from London advised to travel GTR via Cambridge and take GA services via Ely and Thetford.
Buses to operate Felixstowe services calling all stations except Westerfield.
",
"Owing to a {xxx} in the Ipswich area, an amended train service is in place
",
"Contingency Plan GE11 is in operation/ being implemented
with no/ the following variations.
All 1Pxx services stop addl Stowmarket
If 2Wxx term stowmarket…bus service Ipswich-Needham Mkt-Stowmarket",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Ipswich and East Suffolk Junction one of the lines Norwich-bound/Colchester-bound is currently closed. We expect the line 
to reopen at xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return 
train services to normal.
In order to manage the reduced line capacity into Ipswich from the North, we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
Ipswich – Felixstowe: 
Buses are replacing trains between Ipswich and Felixstowe. Please note that rail replacement buses will not call at Westerfield. Customers for 
Westerfield should use trains bound for Lowestoft.
All other Greater Anglia Routes: There is currently a good service running on all other routes.`");

INSERT INTO blockage_contingency_plan
VALUES ("partial", "East Suffolk Junction", "Haughley", "Freight to be diverted via London
Monitor inbound freight, liaise with freight York & SSM Cambridge re-holding points",
"Pilotman
Handsignaller
Barrier man at Claydon CCTV
Barrier man at Regent Street CCTV
Barrier Man at Haughley AHBC
Cow Green GSP Operator (if issue is between Stowmarket and Haughley Jn and SLW is over the Down Main Line)
",
"Points: 1364, 2374, 2379 2384, 2385, 2389, 2392, 2416 (Cow Green GSP)",
"CSL2 mobilised for North via on-call structure
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Ipswich and 
Norwich",
"TFL ticket acceptance (reasonable routes Liverpool St and Kings Cross)
GTR ticket acceptance Kings Cross-Peterborough
EMT Ticket acceptance Norwich-Peterborough
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Norwich customers to/from London advised to travel GTR via Cambridge and GA services Norwich-Cambridge or EMT services to Norwich-Ely.
Peterborough Customers from Ipswich to travel via Norwich and EMT services or via London and GTR services.
",
"Owing to a {xxx} between Diss and Stowmarket/ Stowmarket and Needham Market/ Needham Market and Ipswich, trains between Norwich and 
Ipswich are experiencing 20 minute delays and an amended train service is in place.",
"Contingency Plan GE12 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Haughley and Ipswich one of the lines Norwich-bound/Ipswich-bound is currently closed. We expect the line to reopen at 
xxx / the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train 
services to normal.
In order to manage the reduced line capacity between Ipswich and Diss/ Stowmarket/ Needham Market, we are currently running a reduced train 
service between Norwich and Ipswich and Cambridge and Ipswich. We expect this to continue until approximately xx:xx
London – Norwich services:
Trains are running at an hourly frequency with extended journey times. Customers to/ from Norwich are advised to travel via Cambridge and GTR 
services to/from Kings Cross.
Ipswich – Cambridge services: 
Trains between Ipswich and Cambridge will operate to/from Stowmarket. Customers for Cambridge should change at Stowmarket. 
Ipswich – Peterborough services: 
Trains between Ipswich and Peterborough are not operating. Customers for Peterborough and Ely should travel to Norwich and travel on East 
Midlands Trains services from Norwich to Liverpool Lime St.Customers may also travel via London using GTR services from Kings Cross.
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("partial","Haughley Jn", "Diss", "Consider cancelling 6A33 / 6P40", 
"Pilotman
Handsignaller
Cow Green GSP operator (if needed)
", "Points: 2392, 2396, 2416 (Cow Green GSP), 2451, 2459",
"TFL ticket acceptance (reasonable routes Liverpool St and Kings Cross)
GTR ticket acceptance Kings Cross-Ely
EMT Ticket acceptance Norwich-Ely
Norwich customers to/from London advised to travel FCC via Cambridge and take GA services via Ely and Thetford",
"Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Norwich customers to/from London advised to travel GTR via Cambridge and GA services Norwich-Cambridge or EMT services to Norwich-Ely.",
"Owing to a {xxx} between Diss and Stowmarket, trains between Norwich and Ipswich are experiencing 20 minute delays and an amended train 
service is in place.
",
"Contingency Plan GE13 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Diss and Stowmarket one of the lines Norwich-bound/Ipswich-bound is currently closed. We expect the line to reopen at xxx 
/ the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train services to 
normal.
In order to manage the reduced line capacity between Diss and Stowmarket, we are currently running a reduced train service between Norwich and 
London. We expect this to continue until approximately xx:xx
London – Norwich services:
Trains are running at an hourly frequency with extended journey times. Customers to/ from Norwich are advised to travel via Cambridge and GTR 
services to/from Kings Cross.
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("partial", "Diss", "Trowse", "None",
"Pilotman
Handsignaller
Groundframe Operator at Flordon if needed
",
"Points: 2451, 2459, Flordon Groundframe (if needed), 2837 (Lakenham), 2845.
",
"TFL ticket acceptance (reasonable routes Liverpool St and Kings Cross)
GTR ticket acceptance Kings Cross-Ely
EMT Ticket acceptance Norwich-Ely
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Norwich customers to/from London advised to travel GTR via Cambridge and take GA services via Ely and Thetford",
"Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich).
Norwich customers to/from London advised to travel GTR via Cambridge and GA services Norwich-Cambridge or EMT services to Norwich-Ely",
"Owing to a {xxx} between Diss and Norwich, trains between Norwich and Ipswich are experiencing 20 minute delays and an amended train service 
is in place.",
"Contingency Plan GE14 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Diss and Norwich one of the lines Norwich-bound/Ipswich-bound is currently closed. We expect the line to reopen at xxx / 
the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train services to 
normal.
In order to manage the reduced line capacity between Diss and Stowmarket, we are currently running a reduced train service between Norwich and 
London. We expect this to continue until approximately xx:xx
London – Norwich services:
Trains are running at an hourly frequency with extended journey times. Customers to/ from Norwich are advised to travel via Cambridge and GTR 
services to/from Kings Cross.
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("full", "Liverpool Street", "Stratford", "Stratford" ,
"This plan will require a revised traincrew diagrams and constant stepping up of stock at Stratford to avoid Platform 10A to be kept clear 
for freight.
Must have a train crew manager on site at Stratford to do this. Should also consider having a traincrew manager at Gidea Park.
GA services to start & terminate in Stratford platforms 9 & 10 off peak and also 10A in AM peak
MTR Cross Rail Services to start & terminate in Stratford platforms 5 & 8",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Stratford to ensure that someone is on site should there 
be issues with pointwork.",
"Points: 2146, 2147, 2148, 2152, 2153, 2155, 2156, 2157, 2158, 2159, 2160, 2161, 2163",
"TfL Rail
CSL2 and line status to be declared by control
TFL Rail staff to follow TFL Rail’s PIDD local delivery plan
CAT Team to be deployed where necessary to assist staff and customers.
GREATER ANGLIA
CSL2 mobilised East and West via on-call structure
HQ staff support to Liverpool Street for evening peak
RPIs and MTST support at Liverpool Street, Stratford and Shenfield
Request Driver Manager to Liverpool Street, Stratford and Shenfield via On-Call Operations East
Advise contingency plan on traincrew information monitors (TIM) ) in the following traincrew depots: Liverpool Street, 
Colchester, Clacton, Ilford, Southend, Ipswich and Norwich
Last shuttle train at Wickford must be held to connect with last down services for Southend",
"TfL Rail
Liverpool Street - Stratford
[delay reason] at [location]
Trains will start from Stratford and will call at all stations.
Minor/Severe delays operating on the rest of the line.
This disruption is expected to last until [expected end time].
Customers should use alternative routes. Valid National Rail tickets will be accepted by London Buses, London Underground, Greater Anglia, c2c 
and London Overground services.
Greater Anglia train services between Liverpool St and Shenfield are also affected. Please check Greateranglia.co.uk, tfl.gov.co.uk or 
nationalrail.co.uk for further information.
GREATER ANGLIA
Due to [delay reason] at [location]/between [location and location] all lines are blocked. 
Train services to and from this station/through these stations may be cancelled, delayed by up to [xx] mins or revised. Disruption is expected until 
[expected end time].
The trains that run will start and terminate at Stratford.
This is affecting Greater Anglia train services [from/towards], [between, in both directions] Liverpool Street and Southend Victoria, Braintree, 
Chelmsford, Witham, Colchester, Colchester Town, Harwich, Southminster, Ipswich and Norwich. TfL Rail services from Liverpool Street to Shenfield are also affected. Please check tfl.gov.uk or nationalrail.co.uk for further information.
Customers are advised to use London Underground Central line services on which Greater Anglia tickets will be accepted.
Greater Anglia tickets will be further accepted on:
London Buses on reasonable routes. 
TfL Rail
c2c
Great Northern 
Journey times will be extended by up to [xx]mins.",
"Contingency Plan GE15 is in operation/ being implemented
with no/ the following variations.
Advise customers to postpone their travel where possible or use alternatives",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between London and Stratford the 2 lines London-bound/Stratford-bound are currently closed. We expect the line to reopen at xxx / 
the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train services to 
normal.
In order to manage the reduced line capacity to/from London, we are currently running a reduced train service to/from Stratford and expect this to 
continue until approximately xx:xx
London – Southend/Southminster services: We are running a 20 minute frequency service between London and Southend. A shuttle service is in 
operation between Wickford and Southminster and customers travelling to/from Stratford to these stations should change at Wickford. Customers 
may also use C2C services to Southend from Fenchurch Street. 
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: Services which would normally run between 
London and Harwich are running between Manningtree and Harwich in both directions. Customers wishing to travel to/from these stations should 
change at Manningtree. We are running a limited service on all other routes to and from Stratford and Greater Anglia would like to apologise to 
customers for any overcrowding which occurs as a result. Customers for Norwich may travel on GTR services between Kings Cross and Cambridge 
and transfer to Greater Anglia services between Cambridge and Norwich.
All other Greater Anglia Routes: There is currently a good service running on all other routes.
MTR Crossrail Service Update at xx:xx
Metro Services (London – Shenfield stopping services): We are currently running a ten-minute frequency service stopping at all stations 
between Stratford and Shenfield in both directions. In order to assist customers in making their journey, Greater Anglia tickets are being accepted 
on London Underground and London bus services on all reasonable routes.");

INSERT INTO blockage_contingency_plan
VALUES ("full", "Stratford", "Ilford", "This plan will require a revised traincrew diagrams and constant stepping up of stock at Ilford / Shenfield to avoid platform congestion
This will also involve stepping up of stocks and crew. Must have a train crew manager on site at Ilford to do this. Should also consider 
having a traincrew manager at GideaPark).
Divert freight via T&H where possible… divert GE freight via Bury St Edmunds & across country
Block on freight to adjoining routes
1Kxx Services Southend Victoria - Ilford MUST be 8 car units.",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Ilford to ensure that someone is on site should there be 
issues with pointwork.
",
"Points:, 2183, 2184, 2185, 2199, 2200, 2201
",
"TfL Rail
• CSL2 and line status to be declared by control
• TFL Rail staff to follow TFL Rail’s PIDD local delivery plan
• CAT Team to be deployed where necessary to assist staff and customers.
GREATER ANGLIA
• CSL2 mobilised East and West via on-call structure
• HQ staff support to Liverpool Street for evening peak
• RPIs and MTST support at Liverpool Street, Stratford and Shenfield
• Request Driver Manager to Liverpool Street, Stratford and Shenfield via On-Call Operations East
• Advise contingency plan on traincrew information monitors (TIM) ) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich
• Last shuttle train at Wickford must be held to connect with last down services for Southend",
"London Buses via any reasonable route, including:
Bus 25 between Stratford and Ilford,
Bus 86 between Stratford, Ilford and Romford
London Underground via any reasonable route
Greater Anglia services between Romford and Shenfield
Tfl Rail services between Ilford and Shenfield
c2c services between Fenchurch Street and Upminster 
London Overground services between Romford and Upminster
Great Northern services between King's Cross and Cambridge / Ely (journey time 45 minutes to Cambridge, 65 minutes to Ely) for 
connections on Greater Anglia, Cross Country and East Midlands Trains services between Cambridge / Ely and Norwich. (Journey time 60 Minutes Ely-Norwich
• Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and Norwich.",
"TfL Rail
STRATFORD TO ILFORD, – SUSPENDED
[delay reason] at [location]
Trains will start from Ilford and call at all stations to Shenfield. 
Minor/Severe delays are operating on the rest of the line.
[delay reason] at [location]
This disruption is expected to last until [expected end time].
Customers should use alternative routes from Fenchurch Street for c2c services, London Underground and Local Buses. Valid National Rail tickets 
will be accepted by London Buses, London Underground, DLR, London Overground, Greater Anglia and c2c services. 
Greater Anglia train services between Liverpool St and Shenfield are also affected. Please check Greateranglia.co.uk, tfl.gov.co.uk or 
nationalrail.co.uk for further information.
GREATER ANGLIA
Due to [delay reason] at [location]/between [location and location] all lines are blocked.
Train services to and from this station/through these stations may be cancelled, delayed by up to [xx] mins or revised. Disruption is expected until 
[expected end time].
This is affecting Greater Anglia train services [from/towards], [between, in both directions] Liverpool Street and Southend Victoria, Braintree, 
Chelmsford, Witham, Colchester, Colchester Town, Harwich, Southminster, Ipswich and Norwich.
TfL Rail services from Liverpool Street to Shenfield are also affected. Please check tfl.gov.uk or nationalrail.co.uk for further information.
Greater Anglia tickets will be accepted on:
London Buses and London Underground on reasonable routes. 
TfL Rail
c2c
Great Northern
Journey times will be extended by up to [xx]mins.",
"Contingency Plan GE16 is in operation/ being implemented
with no/ the following variations.
Advise customers to postpone their travel where possible or use alternatives.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Ilford and Stratford the lines are currently closed. We expect the line to reopen at xxx / the line is currently closed and we 
are working to assess the problem / The line has now reopened and we are working to return train services to normal.
Owing to the line closure, we are currently running a reduced train service to/from Shenfield and a limited frequency Metro service to Ilford and 
expect this to continue until approximately xx:xx
London – Southend/Southminster services: We are running a 30 minute frequency service between Ilford and Southend. A shuttle service is in 
operation between Wickford and Southminster and customers travelling to/from Stratford to these stations should change at Wickford. Customers 
may also use C2C services between Southend and Fenchurch Street. Abellio Greater Anglia would like to apologise to customers for the limited
service, extended journey times and any overcrowding which occurs as a result. 
London – Chelmsford, Colchester, Clacton, Ipswich and surrounding branch lines: A limited train service is in operation between Chelmsford, 
Colchester, Clacton, Ipswich and Shenfield. Customers travelling to and from London to these destinations are advised to travel to Witham where a 
rail replacement bus is in operation to Stansted Airport. Customers may then continue their journey using Stansted Express services to/ from 
London Liverpool Street. 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Greater Anglia would like to apologise to customers for the limited service, extended journey times and any overcrowding which occurs as a result. 
London – Norwich
Customers for Norwich may travel on GTR services between Kings Cross and Cambridge and transfer to Greater Anglia services between 
Cambridge and Norwich.
All other Greater Anglia Routes: There is currently a good service running on all other routes.
MTR Crossrail Service Update at xx:xx
Metro Services (London – Shenfield stopping services): We are currently running a 20 minute frequency service stopping at all stations between 
Ilford and Shenfield in both directions. In order to assist customers in making their journey, Greater Anglia tickets are being accepted on London 
Underground and London bus services on all reasonable routes. TfL Bus 86 operates all stations between Stratford and Romford and TfL Bus 25 
from Stratford to Ilford.
");

INSERT INTO blockage_contingency_plan
VALUES ("full", "Ilford", "Gidea Park", "This plan will require a revised traincrew diagrams and constant stepping up of stock at Ilford / Shenfield to avoid platform congestion
This will also involve stepping up of stocks and crew. Must have a train crew manager on site at Ilford to do this. Should also consider 
having a traincrew managers at GideaPark Shenfield and Chadwell Heath)
Freight Services to be diverted cross country where possible",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Ilford & Shenfield to ensure that someone is on site 
should there be issues with pointworK",
"Points at Ilford: 2173, 2177, 2178, 2179, 
Points at Gidea: 2223
Points at Shenfield: 2259, 2261, 2268, 2272,2281, 2282, 2284, 2294, 2295",
"TfL Rail
• CSL2 and line status to be declared by control
• TFL Rail staff to follow TFL Rail’s PIDD local delivery plan
• CAT Team to be deployed where necessary to assist staff and customers.
GREATER ANGLIA
• CSL2 mobilised East and West via on-call structure
• HQ staff support to Liverpool Street for evening peak
• RPIs and MTST support at Liverpool Street, Stratford and Shenfield
• Request Driver Manager to Liverpool Street, Stratford and Shenfield via On-Call Operations East
• Advise contingency plan on traincrew information monitors (TIM) ) in the following traincrew depots: Liverpool Street, Colchester, Clacton, 
Ilford, Southend, Ipswich and Norwich
• Last shuttle train at Wickford must be held to connect with last down services for Southend
",
"London Buses via any reasonable route; Route 86 between Ilford and Romford, Routes 174, 294 496 and 498 run between Gidea Park and 
Romford
London Underground via any reasonable route
Greater Anglia services between Romford and Shenfield
c2c services between Fenchurch Street and Southend Central via Barking and Upminster 
London Overground services between Romford and Upminster
Great Northern services between King's Cross and Cambridge / Ely (journey time 45 minutes to Cambridge, 65 minutes to Ely) for 
connections on Greater Anglia, Cross Country and East Midlands Trains services between Cambridge / Ely and Norwich. (Journey time 60 
Minutes Ely-Norwich
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and Norwich.
",
"ILFORD TO GIDEA PARK, – SUSPENDED
[delay reason] at [location]
Trains will run between Liverpool Street and Ilford.
Trains will run between Gidea Park and Shenfield.
Minor/Severe delays are operating on the rest of the line.
This disruption is expected to last until [expected end time].
Customers should use alternative routes from Fenchurch Street for c2c services, London Underground and Local Buses. Valid National Rail tickets 
will be accepted by London Buses, London Underground, DLR, London Overground, Greater Anglia and c2c services. 
Greater Anglia train services between Liverpool St and Shenfield are also affected. Please check Abelliogreateranglia.co.uk, tfl.gov.co.uk or 
nationalrail.co.uk for further information.
GREATER ANGLIA
Due to [delay reason] at [location]/between [location and location] all lines are blocked.
Train services to and from this station/through these stations may be cancelled, delayed by up to [xx] mins or revised. Disruption is expected until 
[expected end time].
This is affecting Greater Anglia train services [from/towards], [between, in both directions] Liverpool Street and Southend Victoria, Braintree, 
Chelmsford, Witham, Colchester, Colchester Town, Harwich, Southminster, Ipswich and Norwich.
TfL Rail services from Liverpool Street to Shenfield are also affected. Please check tfl.gov.uk or nationalrail.co.uk for further information.
Customers to and from Southend Victoria are advised to use c2c services between Fenchurch Street and Southend.Central.
Greater Anglia tickets will be accepted on:
London Buses and London Underground on reasonable routes. 
TfL Rail
c2c
Great Northern
Journey times will be extended by up to [xx]mins.",
"Contingency Plan GE17 is in operation/ being implemented
with no/ the following variations.
Advise customers to postpone their travel where possible or use alternatives.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Ilford and Gidea Park the lines are currently closed. We expect the line to reopen at xxx / the line is currently closed and 
we are working to assess the problem / The line has now reopened and we are working to return train services to normal.
Owing to the line closure, we are currently running a reduced train service and expect this to continue until approximately xx:xx
London – Southend/Southminster services: We are running a 30 minute frequency service between Shenfield and Southend. A shuttle service is 
in operation between Wickford and Southminster. Customers travelling to/from London to Southend are advised to use C2C services between 
Southend and Fenchurch Street. Customers travelling to/from Southminster and London should change at Wickford and travel to Southend for 
transfer to C2C services to and from London. Greater Anglia would like to apologise to customers for the limited service, extended journey times 
and any overcrowding which occurs as a result. 
London – Chelmsford, Colchester, Clacton, Ipswich and surrounding branch lines: A limited train service is in operation between Chelmsford, 
Colchester, Clacton, Ipswich and Shenfield. Customers travelling to and from London to these destinations are advised to travel to Witham where a 
rail replacement bus is in operation to Stansted Airport. Customers may then continue their journey using Stansted Express services to/ from 
London Liverpool Street. 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Greater Anglia would like to apologise to customers for the limited service, extended journey times and any overcrowding which occurs as a result. 
London – Norwich
Customers for Norwich may travel on GTR services between Kings Cross and Cambridge and transfer to Greater Anglia services between 
Cambridge and Norwich.
All other Greater Anglia Routes: There is currently a good service running on all other routes.
MTR Crossrail Service Update at xx:xx
Metro Services (London – Shenfield stopping services): We are currently running a 20 minute frequency service stopping at all stations between 
Ilford and London in both directions and a 30 minute frequency service between Gidea Park and Shenfield. In order to assist customers in making 
their journey, Greater Anglia tickets are being accepted on London Underground and London bus services on all reasonable routes. TfLBus 86 
operates all stations between Stratford and Romford and TfL Bus 25 from Stratford to Ilford.");

INSERT INTO blockage_contingency_plan 
VALUES ("full", "Gidea Park", "Shenfield","This plan will require a revised traincrew diagrams and constant stepping up of stock at Ilford / Shenfield to avoid platform congestion
This will involve stepping up of stocks and crew. Must have a train crew manager on site at Ilford to do this. Should also consider having 
a traincrew managers at GideaPark and Shenfield)
",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Ilford & Shenfield to ensure that someone is on site 
should there be issues with pointwork",
"Points at Ilford: 2173, 2177, 2178, 2179, 
Points at Gidea: 2223
Points at Shenfield: 2259, 2261, 2268, 2272,2281, 2282, 2284, 2294, 2295",
"TfL Rail
• CSL2 and line status to be declared by control
• TFL Rail staff to follow TFL Rail’s PIDD local delivery plan
• CAT Team to be deployed where necessary to assist staff and customers.
GREATER ANGLIA
• CSL2 mobilised East and West via on-call structure
• HQ staff support to Liverpool Street for evening peak
• RPIs and MTST support at Liverpool Street, Stratford and Shenfield
• Request Driver Manager to Liverpool Street, Stratford and Shenfield via On-Call Operations East
• Advise contingency plan on traincrew information monitors (TIM) ) in the following traincrew depots: Liverpool Street, Colchester, Clacton, 
Ilford, Southend, Ipswich and Norwich
• Last shuttle train at Wickford must be held to connect with last down services for Southend",
"London Buses via any reasonable route, Bus 498 between Gidea Park and Brentwood via Harold Wood
London Underground via any reasonable route
Greater Anglia services between London Liverpool Street and Shenfield
c2c services between Fenchurch Street and Southend Central via Barking and Upminster.
London Overground services between Romford and Upminster
• Great Northern services between King's Cross and Cambridge / Ely (journey time 45 minutes to Cambridge, 65 minutes to Ely) for 
connections on Greater Anglia, Cross Country and East Midlands Trains services between Cambridge / Ely and Norwich. (Journey time 60 
Minutes Ely-Norwich
 • Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services between London and 
Norwich.",
"[delay reason] at [location]
Trains will run between Liverpool Street and Gidea Park
Minor/Severe delays are operating on the rest of the line.
This disruption is expected to last until [expected end time].
Customers should use alternative routes from Fenchurch Street for c2c services, London Underground and Local Buses. Valid National Rail tickets 
will be accepted by London Buses, London Underground, DLR, London Overground, Greater Anglia and c2c services. 
Greater Anglia train services between Liverpool St and Shenfield are also affected. Please check Abelliogreateranglia.co.uk, tfl.gov.co.uk or 
nationalrail.co.uk for further information.
GREATER ANGLIA
Due to [delay reason] at [location]/between [location and location] all lines are blocked.
Train services to and from this station/through these stations may be cancelled, delayed by up to [xx] mins or revised. Disruption is expected until 
[expected end time].
This is affecting Greater Anglia train services [from/towards], [between, in both directions] Liverpool Street and Southend Victoria, Braintree, 
Chelmsford, Witham, Colchester, Colchester Town, Harwich, Southminster, Ipswich and Norwich.
TfL Rail services from Liverpool Street to Shenfield are also affected. Please check tfl.gov.uk or nationalrail.co.uk for further information.
Customers to and from Southend Victoria are advised to use c2c services between Fenchurch Street and Southend.Central
Customers to and from Ipswich and Norwich are advised to travel via Cambridge on Greater Anglia services from Liverpool Street or Great Northern 
services from Kings’s Cross.
And tCambridge
Greater Anglia tickets will be accepted on:
London Buses and London Underground on reasonable routes. 
TfL Rail
c2c
Great Northern
Journey times will be extended by up to [xx]mins.
",
"Contingency Plan GE18 is in operation/ being implemented
with no/ the following variations.
Advise customers to postpone their travel where possible or use alternatives.", 
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Ilford and Gidea Park the lines are currently closed. We expect the line to reopen at xxx / the line is currently closed and 
we are working to assess the problem / The line has now reopened and we are working to return train services to normal.
Owing to the line closure, we are currently running a reduced train service and expect this to continue until approximately xx:xx
.
London – Southend/Southminster services: We are running a 30 minute frequency service between Shenfield and Southend. A shuttle service is 
in operation between Wickford and Southminster. Customers travelling to/from London to Southend are advised to use C2C services between 
Southend and Fenchurch Street. Customers travelling to/from Southminster and London should change at Wickford and travel to Southend for 
transfer to C2C services to and from London. Greater Anglia would like to apologise to customers for the limited service, extended journey times 
and any overcrowding which occurs as a result. 
London – Chelmsford, Colchester, Clacton, Ipswich and surrounding branch lines: A limited train service is in operation between Chelmsford, 
Colchester, Clacton, Ipswich and Shenfield. Customers travelling to and from London to these destinations are advised to travel to Witham where a 
rail replacement bus is in operation to Stansted Airport. Customers may then continue their journey using Stansted Express services to/ from 
London Liverpool Street. 
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Greater Anglia would like to apologise to customers for the limited service, extended journey times and any overcrowding which occurs as a result. 
London – Norwich
Customers for Norwich may travel on GTR services between Kings Cross and Cambridge and transfer to Greater Anglia services between 
Cambridge and Norwich.
All other Greater Anglia Routes: There is currently a good service running on all other routes.
MTR Crossrail Service Update at xx:xx
Metro Services (London – Shenfield stopping services): We are currently running a 10 minute frequency service stopping at all stations between 
Liverpool Street and Gidea Park in both directions. In order to assist customers in making their journey, Greater Anglia tickets are being accepted 
on London Underground and London bus services on all reasonable routes. TfLBus 86 operates all stations between Stratford and Romford and TfL 
Bus 25 from Stratford to Ilford.
");

INSERT INTO blockage_contingency_plan 
VALUES ("full", "Shenfield", "Chelmsford", "Must have a train crew manager on site at Chelmsford to do this.
Divert freight via BurySt Edmunds & across country up to W9 traffic only",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Chelmsford to ensure that someone is on site should 
there be issues with pointwork
",
"Points at Chelmsford: 2349, 2356, 
Points at Witham: 2367, 2368, 2374, 2377, 2381",
"CSL2 mobilised North and Southeast via on-call structure.
HQ staff support to Liverpool Street for evening peak
RPIs and MTST support at Shenfield, Witham and Billericay.
Request Driver Manager to Chelmsford, Witham & Colchester
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich.
Request Octagon staff to attend Colchester Town (when booked unmanned)",
"TFL ticket Acceptance on Metropolitan line between Liverpool St and Kings Cross (must check as operating good service)
Customers London-Norwich to travel via Cambridge and GTR to Kings Cross.
Ticket acceptance on C2C (Essex Thameside routes)
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services)
Establish rail replacement bus link Witham-Billericay.
Establish rail replacement bus link Shenfield, Ingatestone and Chelmsford. Between 15:30 and 16:30hrs, school children travelling London-bound 
from Ingatestone should be given priority.",
"Owing to a {xxx} between Shenfield and Chelmsford, the mainline is currently closed. Trains are operating to and from Chelmsford, Colchester and 
Ipswich. A rail replacement bus service is in preparation/ operation between Billericay and Witham where customers may continue their journey via 
Southend services to and from London. 
Customers for Ingatestone may travel to either Shenfield or Chelmsford where a limited rail-replacement bus service is in preparation/ operation.
Normal services are expected to resume at xxxxxxx.",
"Contingency Plan GE19 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Chelmsford and Shenfield the line is currently closed. We expect the line to reopen at xxx / the line is currently closed and 
we are working to assess the problem / The line has now reopened and we are working to return train services to normal.
In order to manage the reduced line capacity to/from Shenfield and Chelmsford we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
All services are currently suspended between Chelmsford and Shenfield. Customers to and from London are advised that a rail replacement bus 
service is operating between Witham and Billericay connecting with train services between London and Southend.
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Services which would normally run between London and Braintree are running between Witham and Braintree in both directions. Customers wishing 
to travel to/from these stations should change at Witham. 
Services are suspended to/from Colchester Town. Customers are advised to use local buses to and from Colchester. 
Customers wishing to travel to/from Ingatestone are advised to travel to either to Shenfield or to Chelmsford where a limited rail-replacement bus 
service is/ will be in operation.
All other Greater Anglia Routes: There is currently a good service running on all other routes");

INSERT INTO blockage_contingency_plan 
VALUES ("full", "Chelmsford", "Witham",
"INSTRUCTIONS TO CONTROLLERS:
Must have train crew managers on site at Witham & Chelmsford to do this.
Divert freight via BurySt Edmunds & across country up to W9 traffic only",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Chelmsford & Witham to ensure that someone is on site should 
there be issues with pointwork",
"Points at Chelmsford: 2349, 2352
Points at Witham: 2367, 2368, 2374, 2377, 2381, 
Points at Kelvedon: 2384, 2387",
"CSL2 mobilised North via on-call structure
HQ staff support to Liverpool Street for evening peak
RPIs and MTST support at Witham
Request Driver Manager to Chelmsford and Witham via On-Call Operations L1 North
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich.
Request Octagon staff to attend Colchester Town (when booked unmanned)",
"Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services)
Customers London-Norwich to travel via Cambridge and GTR to Kings Cross
Establish rail replacement bus link Witham-Billericay
",
"Owing to a {xxx} between Witham and Chelmsford, the mainline is currently closed. Trains are operating to and from Witham to Colchester, Clacton 
and Ipswich. A rail replacement bus service is in preparation/ operation between Billericay and Witham where customers may continue their journey 
via Southend services to and from London. 
Customers for Hatfield Peveral may travel to either Witham or Chelmsford where a limited rail-replacement bus service is in preparation/ operation.
Normal services are expected to resume at xxxxxxx.",
"Contingency Plan GE20 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Chelmsford and Witham the line is currently closed. We expect the line to reopen at xxx / the line is currently closed and 
we are working to assess the problem / The line has now reopened and we are working to return train services to normal.
In order to manage the reduced line capacity between Shenfield and Chelmsford we are currently running a reduced train service and expect this to 
continue until approximately xx:xx
London – Chelmsford, Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
All services are currently suspended between Chelmsford and Shenfield. Customers to and from London are advised that a rail replacement bus 
service is operating between Witham and Billericay connecting with train services operating between London and Southend.
Services which would normally run between London and Harwich are running between Colchester and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Colchester. 
Services which would normally run between London and Braintree are running between Witham and Braintree in both directions. Customers wishing 
to travel to/from these stations should change at Witham. 
Services are suspended to/from Colchester Town. Customers are advised to use local buses to and from Colchester. 
Customers wishing to travel to/from Ingatestone are advised to travel to either to Shenfield or to Chelmsford where a limited rail-replacement bus 
service is/ will be in operation.
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("full", "Witham", "Colchester", "Must have train crew managers on site at Colchester & Witham
Divert freight via BurySt Edmunds & across country up to W9 traffic only
",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Witham & Colchester to ensure that someone is on site should 
there be issues with pointwork.",
"Points at Witham: 2367, 2368, 2369, 2370
Points at Colchester: 3025, 3026,3029, 3032, 3033, 3059",
"CSL2 mobilised North via on-call structure
HQ staff support to Liverpool Street for evening peak
RPIs and MTST support at Witham
Request Driver Manager to Colchester and Witham via On-Call Operations L1 North
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Southend, Ipswich and Norwich.
Request Octagon staff to attend Colchester Town (when booked unmanned) and Colchester.",
"Customers London-Norwich to travel via Cambridge and GTR to Kings Cross
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services)
Establish rail replacement bus link Witham-Colchester within 60 minutes.",
"Owing to a {xxx} between Witham and Colchester, the mainline is currently closed. Trains are operating to and from Colchester to Clacton, Ipswich 
and Norwich. A rail replacement bus service is in preparation/ operation between Colchester and Witham where customers may continue their 
journey to and from London. 
Normal services are expected to resume at xxxxxxx.",
"Contingency Plan GE21 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Colchester and Witham the line is currently closed. We expect the line to reopen at xxx / the line is currently closed and we 
are working to assess the problem / The line has now reopened and we are working to return train services to normal.
A rail replacement bus service is in preparation/ operation between Colchester and Witham where customers may continue their journey to and from 
London. 
and expect this to continue until approximately xx:xx
London – Colchester, Clacton, Ipswich, Norwich and surrounding branch lines: 
All services are currently suspended between Colchester and Witham. Customers to and from London are advised that a rail replacement bus 
service is operating between Witham and Colchster connecting with train services operating to Clacton, Ipswich and Norwich and from Witham to 
London.
Services which would normally run between London and Harwich are running between Manningtree and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Manningtree. 
Customers travelling to/ from Norwich are advised to travel via Cambridge and connect with Govia Thameslink Railway services to/ from Kings 
Cross.
Customers travelling to Kelvedon or Marks Tey are advised that a rail replacement bus service is in operation calling at all stations between 
Colchester and Witham. 
Services are suspended to/from Colchester Town. Customers are advised to use local buses to and from Colchester. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("full", "Colchester", "Manningtree", "Divert freight via BurySt Edmunds & across country up to W9 traffic only",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Colchester & Manningtree to ensure that someone is on site 
should there be issues with pointwork.",
"Points at Colchester: 3012, 3015, 3023
Points at Manningtree: 1261",
"CSL2 mobilised North via on-call structure
RPIs and MTST support at Manningtree
Request Driver Manager to Colchester and Manningtree via On-Call Operations L1 North
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Ipswich and Norwich.
Request Octagon staff to attend Colchester Town (when booked unmanned) and Colchester.",
"Customers London-Norwich to travel via Cambridge and GTR to Kings Cross
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services)
Establish rail replacement bus link Manningtree and Colchester within 60 minutes.",
"Owing to a {xxx} between Manningtree and Colchester, the mainline is currently closed. Trains are operating to and from Colchester to Clacton, 
Ipswich and Norwich. A rail replacement bus service is in preparation/ operation between Colchester and Manningtree where customers may 
continue their journey to and from London. 
Normal services are expected to resume at xxxxxxx.",
"Contingency Plan GE22 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Colchester and Manningtree the line is currently closed. We expect the line to reopen at xxx / the line is currently closed 
and we are working to assess the problem / The line has now reopened and we are working to return train services to normal.
A rail replacement bus service is in preparation/ operation between Colchester and Manningtree where customers may continue their journey to and 
from London. 
and expect this to continue until approximately xx:xx
London – Ipswich, Norwich and surrounding branch lines: 
All services are currently suspended between Colchester and Manningtree. Customers to and from London are advised that a rail replacement bus 
service is operating between Manningtree and Colchester connecting with train services operating to and from Colchester to London.
Services which would normally run between London and Harwich are running between Manningtree and Harwich in both directions. Customers 
wishing to travel to/from these stations should change at Manningtree. 
Customers travelling to/ from Norwich are advised to travel via Cambridge and connect with GTR services to/ from Kings Cross.
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("full", "Manningtree", "Ipswich",
"Shunting to take place at Manningtree North Jn if available. Shunting can also take place at Mistley. Permission should be obtained from Operations 
on-call level 2 to start passenger services from the down main platform (platform 3) at Manningtree if this is necessary.
Divert freight via BurySt Edmunds & across country up to W9 traffic only",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Manningtree & Ipswich to ensure that someone is on site should 
there be issues with pointwork.",
"Points at Manningtree & Mistley: 1247, 1252, 1254, 1262, 1271, 1272
Points at Ipswich: 1323, 1326, 1327, 1341, 1342, 1343",
"CSL2 mobilised North via on-call structure
RPIs and MTST support at Manningtree
Request Driver Manager to Ipswich and Manningtree via On-Call Operations L1 North
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ilford, 
Ipswich and Norwich.",
"Customers London-Norwich to travel via Cambridge and GTR to Kings Cross
Establish rail replacement bus link Manningtree and Colchester within 60 minutes.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services)",
"Owing to a {xxx} between Manningtree and Ipswich, the mainline is currently closed. Trains are operating at a reduced frequency to and from 
London and Manningtree and to and from, Ipswich and Norwich. A rail replacement bus service is in preparation/ operation between Ipswich and 
Manningtree where customers may continue their journey.
Normal services are expected to resume at xxxxxxx.",
"Contingency Plan GE23 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Ipswich and Manningtree the line is currently closed. We expect the line to reopen at xxx / the line is currently closed and 
we are working to assess the problem / The line has now reopened and we are working to return train services to normal.
A rail replacement bus service is in preparation/ operation between Ipswich and Manningtree where customers may continue their journey to and 
from London and we expect this to continue until approximately xx:xx
London – Ipswich and Norwich: 
All services are currently suspended between Ipswich and Manningtree. Customers to and from London are advised that a rail replacement bus 
service is operating between Manningtree and Colchester connecting with train services operating to and from Manningtree to London.
Customers travelling to/ from Ipswich are advised to travel to Manningtree and connect with rail replacement bus service.
Customers travelling to/ from Norwich are advised to travel via Cambridge and connect with GTR services to/ from Kings Cross.
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("FULL", "Ipswich","Stowmarket", "Will require shunting in and out of the loop at Stowmarket",
"MOM’s or Maintenance staff capable of route setting to be moved / positioned at Ipswich & Stowmarket to ensure that someone is on site should 
there be issues with pointwork",
"Points at Ipswich: 1301, 1302, 1310, 1311, 
Points at Stowmarket: 2384, 2385, 2389
Points at Diss: 2451
",
"CSL2 mobilised North via on-call structure
RPIs and MTSO support at Ipswich and Stowmarket
CSL2 mobilised North via on-call structure
Request Driver Manager to Ipswich and Stowmarket via On-Call Operations L1 North
Advise contingency plan on traincrew information monitors (TIM) in the following traincrew depots: Liverpool Street, Colchester, Clacton, Ipswich 
and Norwich.
",
"Norwich customers to/from London advised to travel GTR via Cambridge and take GA services Norwich-Cambridge or EMT services to NorwichEly.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services)
Local buses (GA tickets not passed)
Local Bus 87/88 operates all stations Ipswich to Stowmarket
Local Bus 459 operates Stowmarket to Diss
Establish rail replacement bus link calling all stations Ipswich-Diss",
"Owing to a {xxx} between Stowmarket and Ipswich, the mainline is currently closed. A rail replacement bus service is in preparation/ operation
between Ipswich and Diss where customers may continue their journey.
Normal services are expected to resume at xxxxxxx.",
"Contingency Plan GE24 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Haughley and Ipswich the line Norwich-bound and Ipswich-bound is currently closed. We expect the line to reopen at xxx / 
the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train services to 
normal.
Train services are operating between London and Ipswich and between Norwich and Diss. Cambridge and Ipswich. We expect this to continue until 
approximately xx:xx
London – Stowmarket, Diss and Norwich:
Customers to/ from Diss and London are advised to travel to Norwich and then via Cambridge and GTR services to/from London Kings Cross.
Customers to/ from Stowmarket are advised to travel to via Cambridge and connect with GTR services to/from London Kings Cross.
Customers to/ from Norwich and London are advised to travel via Cambridge and GTR services to/from London Kings Cross.
Customers travelling between Stowmarket, Diss and Norwich to Ipswich and Colchester are advised that a limited rail-replacement bus service is 
currently in operation/ in preparation.
Ipswich – Cambridge and Peterborough: 
Trains between Ipswich and Cambridge and between Ipswich and Peterborough will operate to/from Stowmarket. A rail replacement bus service is 
in operation/ in preparation between Ipswich and Stowmarket.
All other Greater Anglia Routes: There is currently a good service running on all other routes.");

INSERT INTO blockage_contingency_plan
VALUES ("full", "Stowmarket", "Diss",
"Freight to be diverted via London Where possible",
"None", "Points at Ipswich: 1301, 1302, 1310, 1311 
Points at Diss: 2451
Points at Bury: 27, 28",
"CSL2 mobilised North via on-call structure
RPIs and MTSO support at Ipswich and Stowmarket and unmanned stations where possible",
"Norwich customers to/from London advised to travel GTR via Cambridge and take GA services Norwich-Cambridge or EMT services to NorwichEly.
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services)
Local buses (GA tickets not passed)
 Local Bus 384 operates all stations Bury St Edmunds to Stowmarket
 Local Bus 87/88 operates all stations Ipswich to Stowmarket
 Local Bus 459 operates Stowmarket to Diss
Establish rail replacement bus link calling all stations Ipswich-Diss
Establish rail replacement bus link calling all stations Ipswich-Bury St Edmunds.",
"Owing to a {xxx} between Stowmarket and Haughley, train services between Ipswich and Norwich and between Bury St Edmunds and Ipswich have 
been suspended. A rail replacement bus service is in preparation/ operation to enable customers to continue their journey.
Normal services are expected to resume at xxxxxxx.",
"Contingency Plan GE25 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Haughley and Ipswich the line Norwich-bound and Ipswich-bound is currently closed. We expect the line to reopen at xxx / 
the line is currently closed and we are working to assess the problem / The line has now reopened and we are working to return train services to 
normal.
Train services are operating between London and Ipswich and between Norwich and Diss. Cambridge and Peterborough services are operating as 
far as Bury St Edmunds. We expect this to continue until approximately xx:xx
London – Stowmarket, Diss and Norwich:
Customers to/ from Diss and London are advised to travel to Norwich and then via Cambridge and GTR services to/from London Kings Cross.
Customers to/ from Stowmarket are advised to travel to Ipswich and take local bus routes 87 or 88/ rail replacement bus.
Customers to/ from Norwich and London are advised to travel via Cambridge and GTR services to/from London Kings Cross.
Ipswich – Cambridge and Peterborough: 
Trains between Ipswich and Cambridge and between Ipswich and Peterborough will operate to/from Bury St Edmunds. A rail replacement bus 
service is in operation/ in preparation all stations between Ipswich and Stowmarket. Alternatively, local bus route 384 operates all stations between 
Bury St Edmunds at Stowmarket. Customers should note that Greater Anglia tickets will not be passed on local buses. 
All other Greater Anglia Routes: There is currently a good service running on all other routes.
");

INSERT INTO blockage_contingency_plan
VALUES ("full", "Diss", "Trowse", "6P40 / 6P41 to divert via Ely & Thetford", "None",
"Points at Diss: 2451, 2459",
"CSL2 mobilised North via on-call structure
RPIs and MTSO support at Diss",
"Customers London-Norwich to travel via Cambridge and GTR to Kings Cross
Advance Purchase Ticket holders may travel up to 60 minutes earlier/later than their booked train (Intercity services)
Aim to have bus service in place 60 minutes into the incident:
Establish rail replacement bus link Norwich-Diss",
"Owing to a {xxx} between Diss and Norwich The line is currently closed.
A rail replacement bus service is being established/ in operation between Diss and Norwich.",
"Contingency train service plan GE26 is in operation/ being implemented
with no/ the following variations.",
"Greater Anglia Service Update at xx:xx
Owing to a xxx between Diss and Norwich, the line is currently closed. We expect the line to reopen at xxx / the line is currently closed and we are 
working to assess the problem / The line has now reopened and we are working to return train services to normal.
Train services are operating between London and Diss. We expect this to continue until approximately xx:xx
London – Norwich
Customers to/ from Norwich and London are advised to travel via Cambridge and GTR services to/from London Kings Cross.
Trains are operating at a half hour frequency between London and Diss.
All other Greater Anglia Routes: There is currently a good service running on all other routes.
");
