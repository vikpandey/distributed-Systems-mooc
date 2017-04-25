/*
 * copyright 2014, gash
 * 
 * Gash licenses this file to you under the Apache License,
 * version 2.0 (the "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */
package poke.server.election;

import poke.server.managers.ElectionManager.RState;


public interface ElectionListener {
	void concludeWith(boolean success, Integer LeaderID);
	Integer getElectionId();
	int getLastLogIndex();
	RState getState();
	void setState(RState state);
	void setTermId(Integer electionId);
}