/**
 * 
 */
package peersim.chord;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;

import java.io.File;
import java.io.FileWriter;   // Import the FileWriter class
import java.io.IOException;  // Import the IOException class to handle errors
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;
import java.util.AbstractMap;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

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
	private boolean transferido1 = false;
	private boolean transferido2 = false;
	private boolean transferido3 = false;
	private boolean transferido4 = false;
	private boolean transferido5 = false;
	private boolean transferido6 = false;
	
	private String folder = "";

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
			folder += "./" + (String.valueOf(size)) + "/" + (String.valueOf(CommonState.r.getLastSeed()) + "/");
			File createFolder = new File(folder);
			createFolder.mkdirs();
			
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
					//sender = Network.get(CommonState.r.nextInt(size));
					sender = Network.get(i);
					//target = Network.get(CommonState.r.nextInt(size));
				} while (sender == null || sender.isUp() == false);
				LookUpMessage message = new LookUpMessage(sender,
						((ChordProtocol) target.getProtocol(pid)).chordId, i);
				EDSimulator.add(10, message, sender, pid);
			}
			return false;
		}
		else {
			//partial output - paths
			if(!transferido1) {
				transferido1 = true;
				
				try {
					int size = ChordProtocol.path.length;
					String filename = folder + "output1.txt";
					FileWriter myWriter = new FileWriter(filename);
					
					for(int i = 0; i < size; i++) {
						myWriter.write("node: " + i + "\n");
						for(int j = 0; j < ChordProtocol.path[i].size(); j++) {
							myWriter.write(ChordProtocol.path[i].get(j) + " ");
						}
						myWriter.write("\n");
					}
					myWriter.write("\nThe file was written until the end.\n");
					myWriter.close();
				    System.out.println("Successfully wrote to the file 1.");
				}
				catch(IOException e) {
					System.out.println("An error occurred.");
				    e.printStackTrace();
				}
			}
			//processing and output - convergence
			else if(!transferido2) {
				transferido2 = true;
				try {
					int size = ChordProtocol.path.length;
					String filename = folder + "output2.txt";
					FileWriter myWriter = new FileWriter(filename);
				    
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
				    	myWriter.write("hop " + i + ":\n\ttotal peers that pass through hop (including self): " + counter + "\n\t# of different peers in hop: " + reversePath[i].size() + "\n");
					}
				    myWriter.write("\n");
				    for(int i = 0; i < max; i++) {
						myWriter.write("hop: " + i + "\n");
						//for(int j = 0; j < reversePath[i].size(); j++) {
						//	myWriter.write(reversePath[i].get(j) + " " +  +"\n");
						//}
						//https://stackabuse.com/java-how-to-get-keys-and-values-from-a-map
						for (HashMap.Entry<BigInteger, Integer> pair : reversePath[i].entrySet()) {
							myWriter.write(String.format("%s %s\n", pair.getKey(), pair.getValue()));
						}
						myWriter.write("\n");
					}
					myWriter.write("The file was written until the end.\n");
				    myWriter.close();
				    System.out.println("Successfully wrote to the file 2.");
				}
				catch(IOException e) {
					System.out.println("An error occurred.");
				    e.printStackTrace();
				}
			}
			//removed self node from hop counting
			else if(!transferido3) {
				transferido3 = true;
				try {
					int size = ChordProtocol.path.length;
					String filename = folder + "output3.txt";
					FileWriter myWriter = new FileWriter(filename);
				    
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
				    	int intermediateCounter = 0;
				    	for(Integer value: reversePath[i].values()){
				    	    if(value > 1) {
				    	    	intermediateCounter++;
				    	    }
				    	}
				    	myWriter.write("hop " + i + ":\n\ttotal peers that pass through hop (excluding self): " + (counter - reversePath[i].size()) + "\n\t# of different peers in hop that are intermediate: " + intermediateCounter + "\n");
					}
				    myWriter.write("\n");
				    for(int i = 0; i < max - 1; i++) { //last hop only has leaf nodes
						myWriter.write("hop: " + i + "\n");
						//for(int j = 0; j < reversePath[i].size(); j++) {
						//	myWriter.write(reversePath[i].get(j) + " " +  +"\n");
						//}
						//https://stackabuse.com/java-how-to-get-keys-and-values-from-a-map
						for (HashMap.Entry<BigInteger, Integer> pair : reversePath[i].entrySet()) {
							if(pair.getValue() > 1) {
								myWriter.write(String.format("%s %s\n", pair.getKey(), pair.getValue() - 1));
							}
						}
						myWriter.write("\n");
					}
					myWriter.write("The file was written until the end.\n");
				    myWriter.close();
				    System.out.println("Successfully wrote to the file 3.");
				}
				catch(IOException e) {
					System.out.println("An error occurred.");
				    e.printStackTrace();
				}
			}
			//data file for chart generation
			else if(!transferido4) {
				transferido4 = true;
				try {
					int size = ChordProtocol.path.length;
					String filename = folder + "output4.txt";
					FileWriter myWriter = new FileWriter(filename);
				    
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
				    }
				    for(int i = 1; i < max - 1; i++) { // first and last files don't have useful data
						//for(int j = 0; j < reversePath[i].size(); j++) {
						//	myWriter.write(reversePath[i].get(j) + " " +  +"\n");
						//}
						Map<Integer, Integer> counts = new HashMap<Integer, Integer>();
						for (Integer c : reversePath[i].values()) {
						    int value = counts.get(c) == null ? 0 : counts.get(c);
						    counts.put(c, value + 1);
						}        
						Map<Integer, Integer> treeMap = new TreeMap<>(counts);
						//System.out.println(counts);
						//https://stackabuse.com/java-how-to-get-keys-and-values-from-a-map
						for (Map.Entry<Integer, Integer> pair : treeMap.entrySet()) {
							myWriter.write(String.format("%s %s\n", pair.getKey() - 1, pair.getValue()));
						}
						myWriter.write("\n");
						
					}
					myWriter.write("The file was written until the end.\n");
				    myWriter.close();
				    System.out.println("Successfully wrote to the file 4.");
				}
				catch(IOException e) {
					System.out.println("An error occurred.");
				    e.printStackTrace();
				}
			}
			//statistics
			else if(!transferido5) {
				transferido5 = true;
				try {
					int size = ChordProtocol.path.length;
					String filename = folder + "output5.txt";
					FileWriter myWriter = new FileWriter(filename);
				    
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
				    }
				    //int count = 0;
				    //int total = 0;
					ArrayList<Integer>[] counts = (ArrayList<Integer>[]) new ArrayList[max - 2];
				    for(int i = 1; i < max - 1; i++) { // first and last files don't have useful data
						//for(int j = 0; j < reversePath[i].size(); j++) {
						//	myWriter.write(reversePath[i].get(j) + " " +  +"\n");
						//}
						//for(int j = 0; j < reversePath[i].size(); j++) {
						//	total += reversePath[i].get();
						//	count++;
						//}
				    	counts[i - 1] = new ArrayList<Integer>();
						for (Integer c : reversePath[i].values()) {
						    counts[i - 1].add(c);
						}
						Collections.sort(counts[i - 1], Collections.reverseOrder());
						int total = 0;
						for (int j = 0; j < counts[i - 1].size(); j++) {
							total += counts[i - 1].get(j);
						}
						myWriter.write("hop " + i + ":");
						int sum = 0;
						for (int j = 0; j < counts[i - 1].size(); j++) {
							sum += counts[i - 1].get(j);
							if(total * 0.8 <= sum) {
								myWriter.write(String.format("\n\t80%% reqs passam por %d nos que representam %.2f%% dos nos desse hop", j + 1, 100.0 * (j + 1) / counts[i - 1].size()));
								//exact % (at least 80) //myWriter.write(String.format("\n\t%.2f%% reqs passam por %d nos que representam %.2f%% dos nos desse hop", 100.0 * sum / total, j + 1, 100 * (j + 1) / (double) counts[i - 1].size()));
								break;
							}
						}
						sum = 0;
						for (int j = 0; j < counts[i - 1].size(); j++) {
							sum += counts[i - 1].get(j);
							if(j == 0 || j == 4 || j == 9) {
								myWriter.write(String.format("\n\t%.2f%% reqs sao registradas por %d nos", 100.0 * sum / total, j + 1));
							}
						}
						myWriter.write("\n\n");
					}
					myWriter.write("The file was written until the end.\n");
				    myWriter.close();
				    System.out.println("Successfully wrote to the file 5.");
				}
				catch(IOException e) {
					System.out.println("An error occurred.");
				    e.printStackTrace();
				}
			}
			//raw statistics for python average
			else if(!transferido6) {
				transferido6 = true;
				try {
					int size = ChordProtocol.path.length;
					String filename = folder + "output6.txt";
					FileWriter myWriter = new FileWriter(filename);
				    
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
				    }
					ArrayList<Integer>[] counts = (ArrayList<Integer>[]) new ArrayList[max - 2];
				    for(int i = 1; i < max - 1; i++) { // first and last files don't have useful data
				    	counts[i - 1] = new ArrayList<Integer>();
						for (Integer c : reversePath[i].values()) {
						    counts[i - 1].add(c - 1);
						}
						Collections.sort(counts[i - 1], Collections.reverseOrder());
						int total = 0;
						for (int j = 0; j < counts[i - 1].size(); j++) {
							total += counts[i - 1].get(j);
						}
						int sum = 0;
						for (int j = 0; j < counts[i - 1].size(); j++) {
							sum += counts[i - 1].get(j);
							if(total * 0.8 <= sum) {
								myWriter.write(String.format("%d %d\n", j + 1, counts[i - 1].size()));
								break;
							}
						}
						sum = 0;
						int j;
						for (j = 0; j < counts[i - 1].size(); j++) {
							sum += counts[i - 1].get(j);
							if(j == 0 || j == 4 || j == 9) {
								myWriter.write(String.format("%d %d\n", sum, total));
							}
						}
						if(j <= 4) {
							myWriter.write(String.format("%d %d\n", total, total));
						}
						if(j <= 9) {
							myWriter.write(String.format("%d %d\n", total, total));
						}
						myWriter.write("\n");
					}
					myWriter.write("The file was written until the end.\n");
				    myWriter.close();
				    System.out.println("Successfully wrote to the file 6.");
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
