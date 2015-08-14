/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.ambari.server.state.stack;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

import org.apache.ambari.server.state.stack.upgrade.ClusterGrouping;
import org.apache.ambari.server.state.stack.upgrade.Direction;
import org.apache.ambari.server.state.stack.upgrade.Grouping;
import org.apache.ambari.server.state.stack.upgrade.ServiceCheckGrouping;
import org.apache.ambari.server.state.stack.upgrade.Task;
import org.apache.ambari.server.state.stack.upgrade.UpgradeType;

/**
 * Represents an upgrade pack.
 */
@XmlRootElement(name="upgrade")
@XmlAccessorType(XmlAccessType.FIELD)
public class UpgradePack {

  @XmlElement(name="target")
  private String target;

  @XmlElement(name="target-stack")
  private String targetStack;

  @XmlElement(name="type", defaultValue="rolling")
  private UpgradeType type;

  @XmlElementWrapper(name="order")
  @XmlElement(name="group")
  private List<Grouping> groups;

  /**
   * In the case of a rolling upgrade, will specify processing logic for a particular component.
   * Nonrolling upgrades are simpler so the "processing" is embedded into the  group's "type", which is a function like
   * "stop" or "start".
   */
  @XmlElementWrapper(name="processing")
  @XmlElement(name="service")
  private List<ProcessingService> processing;

  @XmlTransient
  private Map<String, List<String>> m_orders = null;
  @XmlTransient
  private Map<String, Map<String, ProcessingComponent>> m_process = null;
  @XmlTransient
  private boolean m_resolvedGroups = false;

  /**
   * @return the target version for the upgrade pack
   */
  public String getTarget() {
    return target;
  }

  /**
   * @return the target stack, or {@code null} if the upgrade is within the same stack
   */
  public String getTargetStack() {
    return targetStack;
  }

  /**
   * @return the type of upgrade, e.g., "rolling" or "nonrolling"
   */
  public UpgradeType getType() {
    return type;
  }

  /**
   * Gets the groups defined for the upgrade pack.  If a direction is defined
   * for a group, it must match the supplied direction to be returned
   * @param direction the direction to return the ordered groups
   * @return the list of groups
   */
  public List<Grouping> getGroups(Direction direction) {
    List<Grouping> list = new ArrayList<Grouping>();
    if (direction.isUpgrade()) {
      list = groups;
    } else {
      if (type == UpgradeType.ROLLING) {
        list = getDowngradeGroupsForRolling();
      } else if (type == UpgradeType.NONROLLING) {
        list = getDowngradeGroupsForNonrolling();
      }
    }

    List<Grouping> checked = new ArrayList<Grouping>();
    for (Grouping group : list) {
      if (null == group.intendedDirection || direction == group.intendedDirection) {
        checked.add(group);
      }
    }

    return checked;
  }

  /**
   * Calculates the group orders when performing a rolling downgrade
   * <ul>
   *   <li>ClusterGroupings must remain at the same positions (first/last).</li>
   *   <li>When there is a ServiceCheck group, it must ALWAYS follow the same</li>
   *       preceding group, whether for an upgrade or a downgrade.</li>
   *   <li>All other groups must follow the reverse order.</li>
   * </ul>
   * For example, give the following order of groups:
   * <ol>
   *   <li>PRE_CLUSTER</li>
   *   <li>ZK</li>
   *   <li>CORE_MASTER</li>
   *   <li>SERVICE_CHECK_1</li>
   *   <li>CLIENTS</li>
   *   <li>FLUME</li>
   *   <li>SERVICE_CHECK_2</li>
   *   <li>POST_CLUSTER</li>
   * </ol>
   * The reverse would be:
   * <ol>
   *   <li>PRE_CLUSTER</li>
   *   <li>FLUME</li>
   *   <li>SERVICE_CHECK_2</li>
   *   <li>CLIENTS</li>
   *   <li>CORE_MASTER</li>
   *   <li>SERVICE_CHECK_1</li>
   *   <li>ZK</li>
   *   <li>POST_CLUSTER</li>
   * </ol>
   * @return the list of groups, reversed appropriately for a downgrade.
   */
  private List<Grouping> getDowngradeGroupsForRolling() {
    List<Grouping> reverse = new ArrayList<Grouping>();

    int idx = 0;
    int iter = 0;
    Iterator<Grouping> it = groups.iterator();

    while (it.hasNext()) {
      Grouping g = it.next();
      if (ClusterGrouping.class.isInstance(g)) {
        reverse.add(g);
        idx++;
      } else {
        if (iter+1 < groups.size()) {
          Grouping peek = groups.get(iter+1);
          if (ServiceCheckGrouping.class.isInstance(peek)) {
            reverse.add(idx, it.next());
            reverse.add(idx, g);
            iter++;
          } else {
            reverse.add(idx, g);
          }
        }
      }
      iter++;
    }

    return reverse;
  }

  private List<Grouping> getDowngradeGroupsForNonrolling() {
    throw new UnsupportedOperationException("TODO AMBARI-12698");
    /*
    List<Grouping> list = new ArrayList<Grouping>();
    for (Grouping g : groups) {
      list.add(g);
    }
    return list;
    */
  }

  /**
   * Gets the tasks by which services and components should be upgraded.
   * @return a map of service_name -> map(component_name -> process).
   */
  public Map<String, Map<String, ProcessingComponent>> getTasks() {

    if (null == m_process) {
      m_process = new LinkedHashMap<String, Map<String, ProcessingComponent>>();

      if (processing != null) {
        for (ProcessingService svc : processing) {
          if (!m_process.containsKey(svc.name)) {
            m_process.put(svc.name, new LinkedHashMap<String, ProcessingComponent>());
          }

          Map<String, ProcessingComponent> componentMap = m_process.get(svc.name);

          for (ProcessingComponent pc : svc.components) {
            componentMap.put(pc.name, pc);
          }
        }
      }
    }

    return m_process;
  }

  /**
   * A service definition that holds a list of components in the 'order' element.
   */
  public static class OrderService {

    @XmlAttribute(name="name")
    public String serviceName;

    @XmlElement(name="component")
    public List<String> components;
  }

  /**
   * A service definition in the 'processing' element.
   */
  public static class ProcessingService {

    @XmlAttribute
    public String name;

    @XmlElement(name="component")
    public List<ProcessingComponent> components;
  }

  /**
   * A component definition in the 'processing/service' path.
   */
  public static class ProcessingComponent {

    @XmlAttribute
    public String name;

    @XmlElementWrapper(name="pre-upgrade")
    @XmlElement(name="task")
    public List<Task> preTasks;

    @XmlElementWrapper(name="pre-downgrade")
    @XmlElement(name="task")
    public List<Task> preDowngradeTasks;


    @XmlElementWrapper(name="upgrade")
    @XmlElement(name="task")
    public List<Task> tasks;

    @XmlElementWrapper(name="post-upgrade")
    @XmlElement(name="task")
    public List<Task> postTasks;

    @XmlElementWrapper(name="post-downgrade")
    @XmlElement(name="task")
    public List<Task> postDowngradeTasks;
  }
}
