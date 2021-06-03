/**
 * 
 */
package peersim.chord;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;

import java.io.FileWriter;   // Import the FileWriter class
import java.io.IOException;  // Import the IOException class to handle errors
import java.util.List;
import java.util.ArrayList;
import java.util.AbstractMap;
import java.util.HashMap;

import peersim.core.*;
import peersim.config.Configuration;
import peersim.edsim.EDSimulator;

/**
 * @author Andrea
 * 
 */
public class TrafficGenerator implements Control {

	private static final String PAR_PROT = "protocol";

	private final int pid;
	
	private boolean executou = false; //int executou = 0;
	
	private boolean transferido = false;

	/**
	 * 
	 */
	public TrafficGenerator(String prefix) {
		pid = Configuration.getPid(prefix + "." + PAR_PROT);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see peersim.core.Control#execute()
	 */
	public boolean execute() {
		if(!executou) {//if(executou < Network.size()) {
			executou = true;//executou++;
			
			int size = Network.size();
			Node sender, target;
			//int i = 0;
			do {
				//i++;
				//sender = Network.get(CommonState.r.nextInt(size));
				target = Network.get(CommonState.r.nextInt(size));
			} while (target == null || target.isUp() == false);
			for(int i = 0; i < Network.size(); i++) {
				do {
					//i++;
					sender = Network.get(CommonState.r.nextInt(size));
					//target = Network.get(CommonState.r.nextInt(size));
				} while (sender == null || sender.isUp() == false);
				LookUpMessage message = new LookUpMessage(sender,
						((ChordProtocol) target.getProtocol(pid)).chordId);
				EDSimulator.add(10, message, sender, pid);
			}
			return false;
		}
		else {
			if(!transferido) {
				transferido = true;
				
				try {
					int size = ChordProtocol.path.length;
					
					//partial output - paths
					String filename = "output1.txt";
					FileWriter myWriter = new FileWriter(filename);
					
					for(int i = 0; i < size; i++) {
						myWriter.write("node: " + i + "\n");
						for(int j = 0; j < ChordProtocol.path[i].size(); j++) {
							myWriter.write(ChordProtocol.path[i].get(j) + " ");
						}
						myWriter.write("\n");
					}
					myWriter.close();
				    System.out.println("Successfully wrote to the file 1.");
				
				    //processing and final(?) output - convergence
				    filename = "output2.txt";
				    myWriter = new FileWriter(filename);
				    
				    int max = 0;
				    for(int i = 0; i < size; i++) {
						if(max < ChordProtocol.path[i].size()) {
							max = ChordProtocol.path[i].size();
						}
					}
				    HashMap<BigInteger, Integer>[] reversePath = new HashMap[max];
				    for(int i = 0; i < max; i++) {
						reversePath[i] = new HashMap<BigInteger, Integer>();
					}
				    for(int i = 0; i < max; i++) {
				    	int counter = 0;
				    	for(int j = 0; j < size; j++) {
							int currPeerIdx = ChordProtocol.path[j].size() - 1 - i;
							if(currPeerIdx >= 0) {
								counter++;
								BigInteger peer = ChordProtocol.path[j].get(currPeerIdx);
								if(reversePath[i].containsKey(peer)) {
									int currTimes = reversePath[i].get(peer);
									reversePath[i].replace(peer, currTimes + 1);
								}
								else {
									reversePath[i].put(peer, 1);
								}
							}
				    	}
				    	myWriter.write("hop " + i + ":\n\ttotal peers in hop: " + counter + "\n\t# of different peers in hop: " + reversePath[i].size() + "\n");
					}
				    for(int i = 0; i < max; i++) {
						myWriter.write("hop: " + i + "\n");
						//for(int j = 0; j < reversePath[i].size(); j++) {
						//	myWriter.write(reversePath[i].get(j) + " " +  +"\n");
						//}
						for (HashMap.Entry<BigInteger, Integer> pair : reversePath[i].entrySet()) {
							myWriter.write(String.format("%s %s\n", pair.getKey(), pair.getValue()));
						}
						myWriter.write("\n");
					}
				    System.out.println("Successfully wrote to the file 2.");
				}
				catch(IOException e) {
					System.out.println("An error occurred.");
				    e.printStackTrace();
				}
			}
			return false;
		}
	}
	
	/*public boolean execute() {
		int size = Network.size();
		Node sender;
		//for(int i = 0; i < size; i++) {
			//sender = Network.get(i);
		sender = Network.get(CommonState.r.nextInt(size));	
		LookUpMessage message;
			try {
				message = new LookUpMessage(sender,
						new BigInteger(MessageDigest.getInstance("MD5").
								digest("a.mp4".getBytes("UTF-8"))));
				EDSimulator.add(10, message, sender, pid);
			} catch (NoSuchAlgorithmException | UnsupportedEncodingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		//}
		//TODO: file transfer
		/*for(int i = 0; i < Network.size(); i++) {
			for(int j = 0; j < ChordProtocol.path[i].size(); j++) {
				System.out.print(ChordProtocol.path[i].get(j) + " ");
			}
			System.out.println();
		}*/
		//System.exit(0);
		//return false;
	//}

	public <T> List<T> intersection(List<T> list1, List<T> list2) {
        List<T> list = new ArrayList<T>();

        for (T t : list1) {
            if(list2.contains(t)) {
                list.add(t);
            }
        }

        return list;
    }
}
