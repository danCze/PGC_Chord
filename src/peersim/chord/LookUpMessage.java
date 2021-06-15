package peersim.chord;

import java.util.ArrayList;

import java.math.*;
import peersim.core.*;

public class LookUpMessage implements ChordMessage {

	private Node sender;

	private BigInteger targetId;

	private int hopCounter = -1;
	
	private ArrayList<BigInteger> path = new ArrayList<BigInteger>();
	
	private int index;

	public LookUpMessage(Node sender, BigInteger targetId) {
		this.sender = sender;
		this.targetId = targetId;
	}
	
	public LookUpMessage(Node sender, BigInteger targetId, int index) {
		this.sender = sender;
		this.targetId = targetId;
		this.index = index;
	}

	public void increaseHopCounter() {
		hopCounter++;
	}

	/**
	 * @return the senderId
	 */
	public Node getSender() {
		return sender;
	}

	/**
	 * @return the target
	 */
	public BigInteger getTarget() {
		return targetId;
	}

	/**
	 * @return the hopCounter
	 */
	public int getHopCounter() {
		return hopCounter;
	}

	public int getIndex() {
		return index;
	}
	
	public ArrayList<BigInteger> getPath() {
		return path;
	}
	
	/*public void setPath(ArrayList<BigInteger> path) {
		this.path = path;
		return;
	}*/
}
