import matplotlib.pyplot as plt
import json
import sys

def loadJsonToSeries(jsonFile):
    f1 = open(jsonFile)
    
    data1 = json.load(f1)
    f1.close()
    
    xTime = []
    yBitrate = []
    yRetransmits = []
    yRTT = []
    yTotalRetransmits = 0

    for i1 in data1['intervals']:
        xTime.append(i1['sum']['end'])
        yBitrate.append(i1['sum']['bits_per_second'])
        yRetransmits.append(i1['sum']['retransmits'])
        yTotalRetransmits += i1['sum']['retransmits']

        avgRTT1 = 0
        for rtt1 in i1['streams']:
            avgRTT1 += rtt1['rtt']
        avgRTT1 /= len(i1['streams'])
        yRTT.append(avgRTT1)
        
    return xTime, yBitrate, yRetransmits, yTotalRetransmits, yRTT

def toCSV(jsonFile, csvFile):
    xTime, yBitrate, yRetransmits, yTotalRetransmits, yRTT = loadJsonToSeries(
        jsonFile)
    
    totalRetransmissions = 0;
    o = open(csvFile, 'w')
    o.write('Time,Average Bitrate,Average RTT,Average Retransmissions, Total Retransmissions\n')
    for t, b, rtt, r in zip(xTime, yBitrate, yRTT, yRetransmits):
        totalRetransmissions += r
        line = '%.5f,%.5f,%d,%d,%d\n' % (t, b, rtt, r, totalRetransmissions)
        o.write(line)
    
    o.close()
    
def toGraph(series, jsonFile):
    xTime, yBitrate, yRetransmits, yTotalRetransmits, yRTT = loadJsonToSeries(jsonFile)
        
    if series == '-b':
        plt.plot(xTime, yBitrate, label=jsonFile[:jsonFile.rfind("/")])
        plt.ylabel('Bitrate (bits/s)')
        plt.title("Bitrate vs Time")
    elif series == '-r':
        plt.plot(xTime, yRetransmits, label=jsonFile[:jsonFile.rfind("/")])
        plt.ylabel('Retransmits')
        plt.title("Retransmits vs Time")
    elif series == '-rtt':
        plt.plot(xTime, yRTT, label=jsonFile[:jsonFile.rfind("/")])
        plt.ylabel('RTT (ms)')
        plt.title("RTT vs Time")
        
    plt.legend()
    
if len(sys.argv) == 1 or sys.argv[1] == '--help':
    print("""Usage: python3 jsonDigest.py [OPTIONS]  
                 
    OPTIONS:
        --help                                                  Show this help message
        --csv <jsonFile> <csvFile>                              Convert json files to csv file
        --plot [SERIES] <jsonFile>                              Plot visual graph
        --compare [SERIES] <jsonFileTest1> <jsonFileTest2>...   Compare multiple tests in a single graph
        
    SERIES:
        -b                                  Plot bitrate vs time
        -r                                  Plot retransmits vs time
        -rtt                                Plot rtt vs time           
    """)
    sys.exit(1)
elif sys.argv[1] == '--csv':
    toCSV(sys.argv[2], sys.argv[3])
elif sys.argv[1] == '--plot':
    toGraph(sys.argv[2], sys.argv[3])
    plt.show()
elif sys.argv[1] == '--compare':
    plt.xlabel('Time (s)')
    for i in range(3, len(sys.argv)):
        toGraph(sys.argv[2], sys.argv[i])
    plt.show()
else:
    print("""Usage: python3 jsonDigest.py [OPTIONS] 
                
            OPTIONS:
                --help                                                  Show this help message
                --csv <jsonFile> <csvFile>                              Convert json files to csv file
                --plot [SERIES] <jsonFile>                              Plot visual graph
                --compare [SERIES] <jsonFileTest1> <jsonFileTest2>...   Compare multiple tests in a single graph
                
            SERIES:
                -b                                  Plot bitrate vs time
                -r                                  Plot retransmits vs time
                -rtt                                Plot rtt vs time           
    """)
    
sys.exit(0)
