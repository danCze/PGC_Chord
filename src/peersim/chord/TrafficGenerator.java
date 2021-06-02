/**
 * 
 */
package peersim.chord;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;

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
				
				for(int i = 0; i < Network.size(); i++) {
					System.out.println("node: " + i);
					for(int j = 0; j < ChordProtocol.path[i].size(); j++) {
						System.out.print(ChordProtocol.path[i].get(j) + " ");
					}
					System.out.println();
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

}
