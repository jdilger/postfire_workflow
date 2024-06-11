"""
Train features are the features from a older EE JS script. This includes samples that were 
dropped by hand in the code editor. As such, this is messy and hand drawn features should be 
exported to a feature collection at some point (when you have time.)

This is for use with train.py
"""

import ee

ee.Initialize()

table = (ee.FeatureCollection("users/TEST/CAFire/StudyAreas/studyarea"),)
water = ee.FeatureCollection(
    [
        ee.Feature(
            ee.Geometry.Point([-120.61083336270616, 40.18887583179767]),
            {"land_class": 5, "Year": 2018, "system:index": "0"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.60868759549425, 40.187236614643524]),
            {"land_class": 5, "Year": 2018, "system:index": "1"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.60688515103624, 40.18310561171739]),
            {"land_class": 5, "Year": 2018, "system:index": "2"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.60422439969346, 40.1811383790489]),
            {"land_class": 5, "Year": 2018, "system:index": "3"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.60199280179307, 40.183826916069954]),
            {"land_class": 5, "Year": 2018, "system:index": "4"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.59804459012315, 40.18185970431736]),
            {"land_class": 5, "Year": 2018, "system:index": "5"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.59572716153428, 40.17956455184318]),
            {"land_class": 5, "Year": 2018, "system:index": "6"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.59229393399522, 40.177400479826105]),
            {"land_class": 5, "Year": 2018, "system:index": "7"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.58877487576768, 40.177466058780084]),
            {"land_class": 5, "Year": 2018, "system:index": "8"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.58671493924425, 40.18435149623657]),
            {"land_class": 5, "Year": 2018, "system:index": "9"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.5802776376085, 40.18258102191669]),
            {"land_class": 5, "Year": 2018, "system:index": "10"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.57632942593858, 40.18192527896149]),
            {"land_class": 5, "Year": 2018, "system:index": "11"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.57246704495714, 40.18526950176735]),
            {"land_class": 5, "Year": 2018, "system:index": "12"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.585770801671, 40.17549866259036]),
            {"land_class": 5, "Year": 2018, "system:index": "13"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.17021327988925, 40.246272628050704]),
            {"land_class": 5, "Year": 2018, "system:index": "14"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.156480369733, 40.22268406422198]),
            {"land_class": 5, "Year": 2018, "system:index": "15"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.090562400983, 40.212197620711024]),
            {"land_class": 5, "Year": 2018, "system:index": "16"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.11047512070957, 40.24889307236529]),
            {"land_class": 5, "Year": 2018, "system:index": "17"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.19287258164707, 39.884732798001295]),
            {"land_class": 5, "Year": 2018, "system:index": "18"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.18119960801425, 39.885786565602686]),
            {"land_class": 5, "Year": 2018, "system:index": "19"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.9971786119205, 39.72806858482741]),
            {"land_class": 5, "Year": 2018, "system:index": "20"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.97932582871738, 39.73440537137567]),
            {"land_class": 5, "Year": 2018, "system:index": "21"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.66407541855972, 39.67326885082514]),
            {"land_class": 5, "Year": 2018, "system:index": "22"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.6517157994191, 39.68053547174623]),
            {"land_class": 5, "Year": 2018, "system:index": "23"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.68158487900894, 39.699557185268176]),
            {"land_class": 5, "Year": 2018, "system:index": "24"},
        ),
    ]
)
blackoak = ee.FeatureCollection("users/TEST/CAFire/TrainingPoints/blackOak_updated")
vhr = ee.FeatureCollection("users/TEST/CAFire/TrainingPoints/vhr_antelope_lake")
Developed = ee.FeatureCollection(
    [
        ee.Feature(
            ee.Geometry.Point([-120.39252315027204, 39.32554776126197]),
            {"land_class": 3, "Year": 2018, "system:index": "0"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.39604220849958, 39.3245518293047]),
            {"land_class": 3, "Year": 2018, "system:index": "1"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.44599566919294, 39.314326107673175]),
            {"land_class": 3, "Year": 2018, "system:index": "2"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.3337291286656, 39.308017287189095]),
            {"land_class": 3, "Year": 2018, "system:index": "3"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.41029010278669, 39.31086462791249]),
            {"land_class": 3, "Year": 2018, "system:index": "4"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.43935451967207, 39.316666867430335]),
            {"land_class": 3, "Year": 2018, "system:index": "5"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.43686542970624, 39.31723129423422]),
            {"land_class": 3, "Year": 2018, "system:index": "6"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.93778272650843, 39.93654181006053]),
            {"land_class": 3, "Year": 2018, "system:index": "7"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.94653745673304, 39.93687086520138]),
            {"land_class": 3, "Year": 2018, "system:index": "8"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.90817113898402, 39.93910839819987]),
            {"land_class": 3, "Year": 2018, "system:index": "9"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.9074844934762, 39.93265883991364]),
            {"land_class": 3, "Year": 2018, "system:index": "10"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.90319295905238, 39.9357520712672]),
            {"land_class": 3, "Year": 2018, "system:index": "11"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.78118463538294, 39.88321399014812]),
            {"land_class": 3, "Year": 2018, "system:index": "12"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.78989645026331, 39.89487065100833]),
            {"land_class": 3, "Year": 2018, "system:index": "13"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.84167542535465, 40.074930014986855]),
            {"land_class": 3, "Year": 2018, "system:index": "14"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.839937353913, 40.07497927340498]),
            {"land_class": 3, "Year": 2018, "system:index": "15"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83678307611149, 40.074700141897786]),
            {"land_class": 3, "Year": 2018, "system:index": "16"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83823146897953, 40.07662120028825]),
            {"land_class": 3, "Year": 2018, "system:index": "17"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83942236978214, 40.07618609351959]),
            {"land_class": 3, "Year": 2018, "system:index": "18"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83977642137211, 40.07334551686461]),
            {"land_class": 3, "Year": 2018, "system:index": "19"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88751562891696, 40.082075590008245]),
            {"land_class": 3, "Year": 2018, "system:index": "20"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88558443842624, 40.08189499445605]),
            {"land_class": 3, "Year": 2018, "system:index": "21"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.89620598612521, 40.08295393427236]),
            {"land_class": 3, "Year": 2018, "system:index": "22"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.89522966204379, 40.08303602194234]),
            {"land_class": 3, "Year": 2018, "system:index": "23"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.89575537501071, 40.083454667519696]),
            {"land_class": 3, "Year": 2018, "system:index": "24"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.08920201351458, 40.17059241126002]),
            {"land_class": 3, "Year": 2018, "system:index": "25"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.07210284653979, 40.17189442314232]),
            {"land_class": 3, "Year": 2018, "system:index": "26"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.07266074601489, 40.17255026304118]),
            {"land_class": 3, "Year": 2018, "system:index": "27"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.07605105820971, 40.17243549151641]),
            {"land_class": 3, "Year": 2018, "system:index": "28"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.90743608179162, 40.09811744189803]),
            {"land_class": 3, "Year": 2018, "system:index": "29"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.90900249185631, 40.097690679504616]),
            {"land_class": 3, "Year": 2018, "system:index": "30"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.90990371408532, 40.098002544593875]),
            {"land_class": 3, "Year": 2018, "system:index": "31"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.90919561090539, 40.0987739942]),
            {"land_class": 3, "Year": 2018, "system:index": "32"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91125554742882, 40.09667300453468]),
            {"land_class": 3, "Year": 2018, "system:index": "33"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91421670618126, 40.097034116749995]),
            {"land_class": 3, "Year": 2018, "system:index": "34"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.90934581461022, 40.09636113335204]),
            {"land_class": 3, "Year": 2018, "system:index": "35"},
        ),
    ]
)
conifer = (
    ee.FeatureCollection(
        [
            ee.Feature(
                ee.Geometry.Point([-120.90326344104494, 40.081092122984565]),
                {"land_class": 0, "Year": 2018, "system:index": "0"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.89534556003298, 40.07782486401913]),
                {"land_class": 0, "Year": 2018, "system:index": "1"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.88993822665896, 40.078284588326035]),
                {"land_class": 0, "Year": 2018, "system:index": "2"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.88890825839724, 40.074721643765606]),
                {"land_class": 0, "Year": 2018, "system:index": "3"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.8897857252989, 40.06411136406247]),
                {"land_class": 0, "Year": 2018, "system:index": "4"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.88650806588271, 40.06347295244803]),
                {"land_class": 0, "Year": 2018, "system:index": "5"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.90113275670308, 40.06718031598146]),
                {"land_class": 0, "Year": 2018, "system:index": "6"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.90564423226613, 40.06644135135933]),
                {"land_class": 0, "Year": 2018, "system:index": "7"},
            ),
            ee.Feature(
                ee.Geometry.Point([-121.13857418529761, 39.73359534495883]),
                {"land_class": 0, "Year": 2018, "system:index": "8"},
            ),
            ee.Feature(
                ee.Geometry.Point([-121.19052717529479, 39.73804790933362]),
                {"land_class": 0, "Year": 2018, "system:index": "9"},
            ),
            ee.Feature(
                ee.Geometry.Point([-121.03301326774908, 39.782260873937346]),
                {"land_class": 0, "Year": 2018, "system:index": "10"},
            ),
            ee.Feature(
                ee.Geometry.Point([-121.02207604476467, 39.78626400567923]),
                {"land_class": 0, "Year": 2018, "system:index": "11"},
            ),
            ee.Feature(
                ee.Geometry.Point([-121.00040811858827, 39.79260210917901]),
                {"land_class": 0, "Year": 2018, "system:index": "12"},
            ),
            ee.Feature(
                ee.Geometry.Point([-121.03071358317305, 39.88621461406952]),
                {"land_class": 0, "Year": 2018, "system:index": "13"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.99864168896329, 39.39062555989253]),
                {"land_class": 0, "Year": 2018, "system:index": "14"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.98807894434566, 39.53762917520785]),
                {"land_class": 0, "Year": 2018, "system:index": "15"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.9912964423902, 39.53799151498847]),
                {"land_class": 0, "Year": 2018, "system:index": "16"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.95575588473201, 39.543152954823434]),
                {"land_class": 0, "Year": 2018, "system:index": "17"},
            ),
            ee.Feature(
                ee.Geometry.Point([-121.07466050683763, 39.62773112371481]),
                {"land_class": 0, "Year": 2018, "system:index": "18"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.58401491046925, 39.9664150499625]),
                {"land_class": 0, "Year": 2018, "system:index": "19"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.59574947684064, 39.978066646956165]),
                {"land_class": 0, "Year": 2018, "system:index": "20"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.65664904171052, 40.0304328727104]),
                {"land_class": 0, "Year": 2018, "system:index": "21"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.66405224873472, 40.0290397494716]),
                {"land_class": 0, "Year": 2018, "system:index": "22"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.61481666224006, 40.19127768451756]),
                {"land_class": 0, "Year": 2018, "system:index": "23"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.61275672571662, 40.19127768451756]),
                {"land_class": 0, "Year": 2018, "system:index": "24"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.61593246119025, 40.19422807107824]),
                {"land_class": 0, "Year": 2018, "system:index": "25"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.60237121241096, 40.191212118913896]),
                {"land_class": 0, "Year": 2018, "system:index": "26"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.60584735529426, 40.1679323245146]),
                {"land_class": 0, "Year": 2018, "system:index": "27"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.59576224939826, 40.171933082861926]),
                {"land_class": 0, "Year": 2018, "system:index": "28"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.63374232904914, 40.17101489687913]),
                {"land_class": 0, "Year": 2018, "system:index": "29"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.63897800104621, 40.16826026439939]),
                {"land_class": 0, "Year": 2018, "system:index": "30"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.62537383692268, 40.16301303611612]),
                {"land_class": 0, "Year": 2018, "system:index": "31"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.72042429591602, 40.188557763493485]),
                {"land_class": 0, "Year": 2018, "system:index": "32"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.7262393250603, 40.18962323839663]),
                {"land_class": 0, "Year": 2018, "system:index": "33"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.68622252935069, 40.19524283104857]),
                {"land_class": 0, "Year": 2018, "system:index": "34"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.68965575688975, 40.19593122580903]),
                {"land_class": 0, "Year": 2018, "system:index": "35"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.69647929662364, 40.19938948421967]),
                {"land_class": 0, "Year": 2018, "system:index": "36"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.61344169489922, 40.21904337047607]),
                {"land_class": 0, "Year": 2018, "system:index": "37"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.61727188937249, 40.21685598031927]),
                {"land_class": 0, "Year": 2018, "system:index": "38"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.60604952685418, 40.21991994521343]),
                {"land_class": 0, "Year": 2018, "system:index": "39"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.60480498187127, 40.21651189004677]),
                {"land_class": 0, "Year": 2018, "system:index": "40"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.60677908770623, 40.21592201694305]),
                {"land_class": 0, "Year": 2018, "system:index": "41"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.60446165911736, 40.21516828272681]),
                {"land_class": 0, "Year": 2018, "system:index": "42"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.64458801639108, 40.21962867840193]),
                {"land_class": 0, "Year": 2018, "system:index": "43"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.64876153361826, 40.218391634416406]),
                {"land_class": 0, "Year": 2018, "system:index": "44"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.64936234843759, 40.21994817615865]),
                {"land_class": 0, "Year": 2018, "system:index": "45"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.6535251368287, 40.222422184705906]),
                {"land_class": 0, "Year": 2018, "system:index": "46"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.65508081805734, 40.22072643362017]),
                {"land_class": 0, "Year": 2018, "system:index": "47"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.66010191333322, 40.22282358817034]),
                {"land_class": 0, "Year": 2018, "system:index": "48"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.73650072562054, 40.195457945759586]),
                {"land_class": 0, "Year": 2018, "system:index": "49"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.73643635260419, 40.19776895033093]),
                {"land_class": 0, "Year": 2018, "system:index": "50"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.73559950339154, 40.20119433702995]),
                {"land_class": 0, "Year": 2018, "system:index": "51"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.69500275740307, 40.13902960763416]),
                {"land_class": 0, "Year": 2018, "system:index": "52"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.69740601668042, 40.14129332382046]),
                {"land_class": 0, "Year": 2018, "system:index": "53"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.70695468077344, 40.13838984808632]),
                {"land_class": 0, "Year": 2018, "system:index": "54"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.6800038445918, 40.13743839966972]),
                {"land_class": 0, "Year": 2018, "system:index": "55"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.85167583179214, 40.10341247596085]),
                {"land_class": 0, "Year": 2018, "system:index": "56"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.86116821249709, 40.10520969139061]),
                {"land_class": 0, "Year": 2018, "system:index": "57"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.86284191092238, 40.105172763985]),
                {"land_class": 0, "Year": 2018, "system:index": "58"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.86060763081298, 40.10348844267642]),
                {"land_class": 0, "Year": 2018, "system:index": "59"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.86157322605834, 40.10446498483656]),
                {"land_class": 0, "Year": 2018, "system:index": "60"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.70774798972263, 40.1036574032491]),
                {"land_class": 0, "Year": 2018, "system:index": "61"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.70287709815159, 40.10393641603226]),
                {"land_class": 0, "Year": 2018, "system:index": "62"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.70070987326756, 40.10705471633349]),
                {"land_class": 0, "Year": 2018, "system:index": "63"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.72208171469822, 40.10355892787594]),
                {"land_class": 0, "Year": 2018, "system:index": "64"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.72334503514423, 40.10059639375627]),
                {"land_class": 0, "Year": 2018, "system:index": "65"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.73129683601559, 40.10313219961181]),
                {"land_class": 0, "Year": 2018, "system:index": "66"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.74234008193099, 40.10236775386626]),
                {"land_class": 0, "Year": 2018, "system:index": "67"},
            ),
            ee.Feature(
                ee.Geometry.Point([-120.71014303344157, 40.11870682842589]),
                {"land_class": 0, "Year": 2018, "system:index": "68"},
            ),
        ]
    )
)
WoodyWetland = ee.FeatureCollection(
    [
        ee.Feature(
            ee.Geometry.Point([-120.92689378027092, 39.99848826876039]),
            {"land_class": 7, "Year": 2018, "system:index": "0"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92268826240604, 39.995455409896294]),
            {"land_class": 7, "Year": 2018, "system:index": "1"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92013759740536, 39.99307804102169]),
            {"land_class": 7, "Year": 2018, "system:index": "2"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91683142138851, 39.9890372796467]),
            {"land_class": 7, "Year": 2018, "system:index": "3"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.96641969878999, 39.74717221595084]),
            {"land_class": 7, "Year": 2018, "system:index": "4"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.96459579665986, 39.74796000207776]),
            {"land_class": 7, "Year": 2018, "system:index": "5"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.97349440787116, 39.7163093969384]),
            {"land_class": 7, "Year": 2018, "system:index": "6"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.67252028908058, 39.691839883093365]),
            {"land_class": 7, "Year": 2018, "system:index": "7"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91799920458101, 40.08400652753503]),
            {"land_class": 7, "Year": 2018, "system:index": "8"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91885751146577, 40.08361251143328]),
            {"land_class": 7, "Year": 2018, "system:index": "9"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92010205644868, 40.08334983276523]),
            {"land_class": 7, "Year": 2018, "system:index": "10"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92085307497285, 40.08336625021167]),
            {"land_class": 7, "Year": 2018, "system:index": "11"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92252677339815, 40.081872246373095]),
            {"land_class": 7, "Year": 2018, "system:index": "12"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92475837129854, 40.08146180001759]),
            {"land_class": 7, "Year": 2018, "system:index": "13"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92347091097139, 40.08137971044957]),
            {"land_class": 7, "Year": 2018, "system:index": "14"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83030756033935, 40.0676117647346]),
            {"land_class": 7, "Year": 2018, "system:index": "15"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83105857886352, 40.068605242689586]),
            {"land_class": 7, "Year": 2018, "system:index": "16"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83134825743713, 40.06992712064268]),
            {"land_class": 7, "Year": 2018, "system:index": "17"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83082254447021, 40.06921281710843]),
            {"land_class": 7, "Year": 2018, "system:index": "18"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83145554579772, 40.07103550784848]),
            {"land_class": 7, "Year": 2018, "system:index": "19"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83168085135497, 40.07247211234152]),
            {"land_class": 7, "Year": 2018, "system:index": "20"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83349402464904, 40.07698748224239]),
            {"land_class": 7, "Year": 2018, "system:index": "21"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83429868735351, 40.07756214420778]),
            {"land_class": 7, "Year": 2018, "system:index": "22"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83423747879533, 40.08191211331182]),
            {"land_class": 7, "Year": 2018, "system:index": "23"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.83446278435258, 40.082609866028974]),
            {"land_class": 7, "Year": 2018, "system:index": "24"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.93745789569846, 39.95175987540741]),
            {"land_class": 7, "Year": 2018, "system:index": "25"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.93823037189475, 39.95105255884066]),
            {"land_class": 7, "Year": 2018, "system:index": "26"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.94258627933493, 39.94669664235426]),
            {"land_class": 7, "Year": 2018, "system:index": "27"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.9422214989089, 39.94739577886974]),
            {"land_class": 7, "Year": 2018, "system:index": "28"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.94517192882529, 39.945026910944634]),
            {"land_class": 7, "Year": 2018, "system:index": "29"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.94834766429892, 39.94517496759301]),
            {"land_class": 7, "Year": 2018, "system:index": "30"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.94950637859336, 39.94515851687014]),
            {"land_class": 7, "Year": 2018, "system:index": "31"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.95325074237815, 39.94501868556587]),
            {"land_class": 7, "Year": 2018, "system:index": "32"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.93567648769334, 39.94286713743087]),
            {"land_class": 7, "Year": 2018, "system:index": "33"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.93555847049669, 39.94259569084135]),
            {"land_class": 7, "Year": 2018, "system:index": "34"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.93599835277513, 39.9424558542992]),
            {"land_class": 7, "Year": 2018, "system:index": "35"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.93645969272569, 39.94219263179752]),
            {"land_class": 7, "Year": 2018, "system:index": "36"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.02431273917426, 39.948207398969]),
            {"land_class": 7, "Year": 2018, "system:index": "37"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.02601862410773, 39.94919439135224]),
            {"land_class": 7, "Year": 2018, "system:index": "38"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.02579331855048, 39.948667997186696]),
            {"land_class": 7, "Year": 2018, "system:index": "39"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.02699494818916, 39.94907924297466]),
            {"land_class": 7, "Year": 2018, "system:index": "40"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.02802491645087, 39.9494904862903]),
            {"land_class": 7, "Year": 2018, "system:index": "41"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.02815366248359, 39.95014213070473]),
            {"land_class": 7, "Year": 2018, "system:index": "42"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.03036380271186, 39.950026983922484]),
            {"land_class": 7, "Year": 2018, "system:index": "43"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.03194094161262, 39.94935254887699]),
            {"land_class": 7, "Year": 2018, "system:index": "44"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.03654361228217, 39.95011745641055]),
            {"land_class": 7, "Year": 2018, "system:index": "45"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88320409030621, 40.12409941482008]),
            {"land_class": 7, "Year": 2018, "system:index": "46"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88263546199505, 40.12447678897958]),
            {"land_class": 7, "Year": 2018, "system:index": "47"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88133727283184, 40.1257073423381]),
            {"land_class": 7, "Year": 2018, "system:index": "48"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88122998447125, 40.1263390177434]),
            {"land_class": 7, "Year": 2018, "system:index": "49"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.8814552900285, 40.12692146648703]),
            {"land_class": 7, "Year": 2018, "system:index": "50"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88119779796307, 40.12729062155753]),
            {"land_class": 7, "Year": 2018, "system:index": "51"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88166986674969, 40.1274136728022]),
            {"land_class": 7, "Year": 2018, "system:index": "52"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.8814552900285, 40.128012519012934]),
            {"land_class": 7, "Year": 2018, "system:index": "53"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88136945934002, 40.12868518928691]),
            {"land_class": 7, "Year": 2018, "system:index": "54"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.8812943574876, 40.12936605607774]),
            {"land_class": 7, "Year": 2018, "system:index": "55"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88070427150433, 40.12931683702036]),
            {"land_class": 7, "Year": 2018, "system:index": "56"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.88075791568463, 40.12781563864908]),
            {"land_class": 7, "Year": 2018, "system:index": "57"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.25484582502088, 40.11431372585052]),
            {"land_class": 7, "Year": 2018, "system:index": "58"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.25452127773008, 40.11444090307059]),
            {"land_class": 7, "Year": 2018, "system:index": "59"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.25598576385221, 40.113907577651986]),
            {"land_class": 7, "Year": 2018, "system:index": "60"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.25311043578824, 40.11490038007734]),
            {"land_class": 7, "Year": 2018, "system:index": "61"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.24871598483412, 40.13766650903483]),
            {"land_class": 7, "Year": 2018, "system:index": "62"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.24808030129759, 40.137761859210585]),
            {"land_class": 7, "Year": 2018, "system:index": "63"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.24760983492286, 40.138262197862296]),
            {"land_class": 7, "Year": 2018, "system:index": "64"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.24768225456626, 40.138812377714366]),
            {"land_class": 7, "Year": 2018, "system:index": "65"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.24707071091086, 40.1393373058047]),
            {"land_class": 7, "Year": 2018, "system:index": "66"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.24684892962159, 40.1404762971563]),
            {"land_class": 7, "Year": 2018, "system:index": "67"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.24541394779862, 40.140334815402895]),
            {"land_class": 7, "Year": 2018, "system:index": "68"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.24695621798219, 40.14013797073417]),
            {"land_class": 7, "Year": 2018, "system:index": "69"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.22046231237823, 40.30160454812526]),
            {"land_class": 7, "Year": 2018, "system:index": "70"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.22085927931244, 40.3018909297382]),
            {"land_class": 7, "Year": 2018, "system:index": "71"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.22102557627136, 40.30154522606794]),
            {"land_class": 7, "Year": 2018, "system:index": "72"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.22024773565704, 40.30108905816267]),
            {"land_class": 7, "Year": 2018, "system:index": "73"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.22009216753418, 40.301434764167226]),
            {"land_class": 7, "Year": 2018, "system:index": "74"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.22251688448364, 40.30279506943512]),
            {"land_class": 7, "Year": 2018, "system:index": "75"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.2232652207988, 40.30295053115024]),
            {"land_class": 7, "Year": 2018, "system:index": "76"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.21619454966066, 40.303664308965615]),
            {"land_class": 7, "Year": 2018, "system:index": "77"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.21645204172609, 40.30303223880965]),
            {"land_class": 7, "Year": 2018, "system:index": "78"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.2172111068773, 40.30299541900663]),
            {"land_class": 7, "Year": 2018, "system:index": "79"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.8705096089584, 39.9410172771552]),
            {"land_class": 7, "Year": 2018, "system:index": "80"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.87180779812161, 39.94090211501411]),
            {"land_class": 7, "Year": 2018, "system:index": "81"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.87291286823574, 39.94139566568272]),
            {"land_class": 7, "Year": 2018, "system:index": "82"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.87376044628445, 39.941930341556365]),
            {"land_class": 7, "Year": 2018, "system:index": "83"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.87714078498789, 39.9437111933708]),
            {"land_class": 7, "Year": 2018, "system:index": "84"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.87753775192209, 39.94483808258227]),
            {"land_class": 7, "Year": 2018, "system:index": "85"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.87560656143137, 39.94464478538671]),
            {"land_class": 7, "Year": 2018, "system:index": "86"},
        ),
    ]
)
barren = ee.FeatureCollection("users/TEST/CAFire/TrainingPoints/barrenLandFireDerived")
val = ee.FeatureCollection(
    "users/TEST/CAFire/TrainingPoints/validation_cafires_updating"
)
imageVisParam = {
    "opacity": 1,
    "bands": ["Second_swir1", "Second_nir", "Second_red"],
    "min": 44,
    "max": 3549,
    "gamma": 1.6,
}
barren2 = ee.FeatureCollection(
    [
        ee.Feature(
            ee.Geometry.Point([-120.91509019450399, 39.54410107967802]),
            {"Year": 2018, "land_class": 2, "system:index": "0"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91210757807943, 39.54336474509252]),
            {"Year": 2018, "land_class": 2, "system:index": "1"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91382419184896, 39.544705033674326]),
            {"Year": 2018, "land_class": 2, "system:index": "2"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91238652781698, 39.54439892066188]),
            {"Year": 2018, "land_class": 2, "system:index": "3"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91299807147237, 39.54583019422478]),
            {"Year": 2018, "land_class": 2, "system:index": "4"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.913652530472, 39.54367086266682]),
            {"Year": 2018, "land_class": 2, "system:index": "5"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.9128585966036, 39.54323236950706]),
            {"Year": 2018, "land_class": 2, "system:index": "6"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91340576724264, 39.54442374068616]),
            {"Year": 2018, "land_class": 2, "system:index": "7"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91463341357962, 39.549498513771724]),
            {"Year": 2018, "land_class": 2, "system:index": "8"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.9148104393746, 39.54989560391077]),
            {"Year": 2018, "land_class": 2, "system:index": "9"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91467632892386, 39.5503133733746]),
            {"Year": 2018, "land_class": 2, "system:index": "10"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92358660359162, 39.54235647716197]),
            {"Year": 2018, "land_class": 2, "system:index": "11"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92458438534516, 39.54290253171634]),
            {"Year": 2018, "land_class": 2, "system:index": "12"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92288922924774, 39.54362232433704]),
            {"Year": 2018, "land_class": 2, "system:index": "13"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.92537831921356, 39.543787792849606]),
            {"Year": 2018, "land_class": 2, "system:index": "14"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.08674420039199, 40.17368186152048]),
            {"Year": 2018, "land_class": 2, "system:index": "15"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.0878814570143, 40.17373924625322]),
            {"Year": 2018, "land_class": 2, "system:index": "16"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.0870338789656, 40.173444124253564]),
            {"Year": 2018, "land_class": 2, "system:index": "17"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.05934089604693, 40.16778298238437]),
            {"Year": 2018, "land_class": 2, "system:index": "18"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.05830019894915, 40.168065831251255]),
            {"Year": 2018, "land_class": 2, "system:index": "19"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.05867570821124, 40.16831178582962]),
            {"Year": 2018, "land_class": 2, "system:index": "20"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.0553014892705, 40.167725592615355]),
            {"Year": 2018, "land_class": 2, "system:index": "21"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.05466848794299, 40.16740584872836]),
            {"Year": 2018, "land_class": 2, "system:index": "22"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.05503863278705, 40.16683604499101]),
            {"Year": 2018, "land_class": 2, "system:index": "23"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.0557560062752, 40.16495527428203]),
            {"Year": 2018, "land_class": 2, "system:index": "24"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.05607250693896, 40.16517254416144]),
            {"Year": 2018, "land_class": 2, "system:index": "25"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.05680743220904, 40.16545950331378]),
            {"Year": 2018, "land_class": 2, "system:index": "26"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.05644265178302, 40.165352918627356]),
            {"Year": 2018, "land_class": 2, "system:index": "27"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.04372216175341, 40.152850161920476]),
            {"Year": 2018, "land_class": 2, "system:index": "28"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.04443026493334, 40.15358818835976]),
            {"Year": 2018, "land_class": 2, "system:index": "29"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.0459001154735, 40.154301606293956]),
            {"Year": 2018, "land_class": 2, "system:index": "30"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.04564262340807, 40.15517081801636]),
            {"Year": 2018, "land_class": 2, "system:index": "31"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.04408694217943, 40.15412120246684]),
            {"Year": 2018, "land_class": 2, "system:index": "32"},
        ),
        ee.Feature(
            ee.Geometry.Point([-121.04002071331286, 40.15331757959661]),
            {"Year": 2018, "land_class": 2, "system:index": "33"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.90905613603661, 40.09502335390641]),
            {"Year": 2018, "land_class": 2, "system:index": "34"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91011829080651, 40.09373479301173]),
            {"Year": 2018, "land_class": 2, "system:index": "35"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.91006464662621, 40.0949412806916]),
            {"Year": 2018, "land_class": 2, "system:index": "36"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.64237774694516, 39.591693485404306]),
            {"Year": 2018, "land_class": 2, "system:index": "37"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.63516796911313, 39.588187891220336]),
            {"Year": 2018, "land_class": 2, "system:index": "38"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.64709843481137, 39.595331178617066]),
            {"Year": 2018, "land_class": 2, "system:index": "39"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.64598263586117, 39.599762292263875]),
            {"Year": 2018, "land_class": 2, "system:index": "40"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.65070332372738, 39.598770276523226]),
            {"Year": 2018, "land_class": 2, "system:index": "41"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.60808848566899, 39.640289698809895]),
            {"Year": 2018, "land_class": 2, "system:index": "42"},
        ),
    ]
)
grassland = (
    ee.Geometry.MultiPoint(
        [
            [-121.09237683932326, 40.174821349271696],
            [-121.09069241206191, 40.175149255870686],
            [-121.08976973216079, 40.174288497668954],
            [-120.85561232379939, 40.09691661345021],
            [-120.84789829067256, 40.096465222102225],
            [-120.8492930393603, 40.097942491741904],
            [-120.83342315737696, 40.09689720498089],
            [-120.82398178164453, 40.10149302047582],
            [-120.80925987699555, 40.126612654444095],
            [-120.8125643585019, 40.14114771193821],
        ]
    ),
)
deciduous = ee.FeatureCollection(
    [
        ee.Feature(
            ee.Geometry.Point([-120.68895234357683, 40.06823344721681]),
            {"land_class": 6, "Year": 2018, "system:index": "0"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.69018615972368, 40.068196499747316]),
            {"land_class": 6, "Year": 2018, "system:index": "1"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.69075478803484, 40.0686275523112]),
            {"land_class": 6, "Year": 2018, "system:index": "2"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.6913609672722, 40.06819239447168]),
            {"land_class": 6, "Year": 2018, "system:index": "3"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.68967654001085, 40.06882870924085]),
            {"land_class": 6, "Year": 2018, "system:index": "4"},
        ),
        ee.Feature(
            ee.Geometry.Point([-120.69064213525621, 40.06785576102838]),
            {"land_class": 6, "Year": 2018, "system:index": "5"},
        )
    ]
)
f = ee.ImageCollection("users/TEST/CAFire/SeasonComposites/Fall_Full")
s = ee.ImageCollection("users/TEST/CAFire/SeasonComposites/Summer_Full")
image = ee.Image("users/TEST/CAFire/SeasonComposites/Summer_Full/LS_Summer_2001181242")
image2 = ee.Image(
    "users/TEST/CAFire/SeasonComposites/Fall_SA_Bounds/Landsat_SR_fall_2000_2000"
)
studyArea = ee.FeatureCollection("users/TEST/CAFire/StudyAreas/finalStudyArea")
ceo = ee.FeatureCollection(
    "users/TEST/CAFire/TrainingPoints/ceo-nasa-post-fire-recovery-sample-data-2019-01-09-v4"
)
ceo2 = ee.FeatureCollection("users/TEST/CAFire/ceoMergedFinal")
lc07 = ee.FeatureCollection("users/TEST/CAFire/TrainingPoints/LC_2007_Samples")
lc08 = ee.FeatureCollection("users/TEST/CAFire/TrainingPoints/LC_2008_Samples")
lc14 = ee.FeatureCollection("users/TEST/CAFire/TrainingPoints/LC_2014_Samples")
